import io

def test_upload_txt(client):
	"""
	Test the upload route of the project
	"""

	content = b"This is a test file.\nThe project is using FAISS for vector database storage, searching and retrieval."
	data = {
		"files": (io.BytesIO(content), "sample.txt")
	}

	response = client.post("/upload/", data=data, content_type="multipart/form-data")

	assert response.status_code in [200]
	assert isinstance(response.json["Response"], list)
	assert any(
		item.get("filename") == "sample.txt" and
		item.get("status").lower() == "success"
		for item in response.json["Response"]
	)