from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename

from app.text.file import extract_text
from app.core.chunker import chunk_doc
from app.core.embedder import embeddings_from_chunks
from app.core.retriever import save_to_vectorDB
from app.db.database import store_document_metadata
from app.utils.page_count import count_pdf_pages, est_doc_pages, est_text_pages
from app.utils.constants import MAX_PAGES

upload_blueprint = Blueprint("upload", __name__)

@upload_blueprint.route("/", methods = ["POST"])
def upload_document():
	if "files" not in request.files:
		return jsonify({"Error":"Files not found in request"}), 400
	
	if len(request.files.getlist("files")) > 20:
		return jsonify({"Error":"Max 20 files allowed"}), 400


	files = request.files.getlist("files")
	responses = []

	for file in files:
		
		fileName = secure_filename(file.filename)

		fileContent = file.read()

		extension = file.filename.split('.')[-1]
		if extension == "pdf":
			page_count = count_pdf_pages(fileContent)
			if count_pdf_pages(fileContent) > MAX_PAGES:
				responses.append({
					"filename":fileName,
					"status":"Failed",
					"reason":"Pages more than 1000.(Limit reached)"
				})
				continue
		elif extension == "docx":
			page_count = est_doc_pages(fileContent)
			if est_doc_pages(fileContent) > MAX_PAGES:
				responses.append({
					"filename":fileName,
					"status":"Failed",
					"reason":"Pages more than 1000.(Limit reached)"
				})
				continue
		elif extension == "txt":
			page_count = est_text_pages(fileContent)
			if est_text_pages(fileContent) > MAX_PAGES:
				responses.append({
					"filename":fileName,
					"status":"Failed",
					"reason":"Pages more than 1000.(Limit reached)"
				})
				continue
			
		file.stream.seek(0)
		text = extract_text(fileName, fileContent)
		if not text:
			responses.append({
				"filename":fileName,
				"status":"Failed",
				"reason":"Text not found"
			})
			continue
		
		
		chunks = chunk_doc(text)
		embeddings = embeddings_from_chunks(chunks)
		save_to_vectorDB(fileName, chunks, embeddings)
		store_document_metadata(fileName, page_count, len(chunks))
		
		responses.append({
            "filename": fileName,
            "status": "Success",
            "chunks": len(chunks)
        })

	return jsonify({"Response": responses}), 200