from flask import Blueprint, request, jsonify
import pickle
import numpy as np
import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

from app.utils.constants import VECTOR_DB_PATH, QUERY_TOP_K
from app.core.embedder import embeddings_from_chunks

load_dotenv()
query_blueprint = Blueprint("query", __name__)

@query_blueprint.route("/", methods = ["POST"])
def handle_query():
	data = request.get_json()

	question = data.get("question")
	if not question:
		return jsonify({"Error":"Question not provided."}), 400

	ques_embedding = embeddings_from_chunks([question])[0]
	if not ques_embedding:
		return jsonify({"Error":"Cannot create question embedding."}), 400
	
	try:
		with open(VECTOR_DB_PATH, "rb") as vector_file:
			store = pickle.load(vector_file)
	except Exception as e:
		return jsonify({"Error":f"Error occured {e}"}), 500
	
	ques_vec = np.array([ques_embedding]).astype("float32")
	_, I = store["index"].search(ques_vec, QUERY_TOP_K)

	retrieved_chunks = []
	for idx in I[0]:
		if 0 <= idx < len(store["chunks"]):
			retrieved_chunks.append(store["chunks"][idx])
	if len(retrieved_chunks) == 0:
		return jsonify({"Error": "Relevant chunks not found"}), 404
	
	context = '\n'.join(f"{i + 1} {chunk}" for i, chunk in enumerate(retrieved_chunks))
	prompt = (
		f"Anwer the question with given context\n\n"
		f"{context}\n"
		f"Question: {question}"
	)

	try:
		client = InferenceClient(
			provider="together",
			api_key=os.environ["HF_TOKEN"],
		)

		completion = client.chat.completions.create(
			model="mistralai/Mistral-7B-Instruct-v0.3",
			messages=[
				{
					"role": "user",
					"content": prompt
				}
			],
		)
		answer = completion.choices[0].message

	except Exception as e:
		return jsonify({"Error": f"LLM error {e}"}), 500
	
	return jsonify({
		"Question": question,
		"Answer": answer,
		"source_chunks": retrieved_chunks
	}), 200