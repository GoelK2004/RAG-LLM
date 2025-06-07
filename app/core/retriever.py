import os
import pickle
import faiss
import numpy as np
from flask import jsonify

from app.utils.constants import VECTOR_DB_PATH

def save_to_vectorDB(doc_id: str, chunks: list[str], embeddings: list[list[float]]) -> None:
	"""
	Stores the embedding in binary format.
	Arguments:
		doc_id(str): Name of the document
		chunks: List of chunks
		embeddings: Embeddings of each chunks in list format
	"""
		
	if not os.path.exists(VECTOR_DB_PATH) or os.stat(VECTOR_DB_PATH).st_size == 0:
		print("[INFO] Creating new vector DB")
		store = {
			"index": faiss.IndexFlatL2(len(embeddings[0])),
			"chunks": [],
			"doc_ids": []
		}
	
	else:
		try:
			with open(VECTOR_DB_PATH, "rb") as vector_file:
				store = pickle.load(vector_file)
		except Exception as e:
			raise RuntimeError(f"Vector DB corrupted or unreadable: {e}")
	
	np_embeddings = np.array(embeddings).astype("float32")

	store["index"].add(np_embeddings)
	store["chunks"].extend(chunks)
	store["doc_ids"].extend([doc_id] * len(chunks))
	
	with open(VECTOR_DB_PATH, "wb") as vector_file:
		pickle.dump(store, vector_file)