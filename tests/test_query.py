import io

def test_query_handling(client):
	"""
	Test the query route of the project
	"""
	
	content = b"This is a test file.\nThe project is using FAISS for vector database storage, searching and retrieval."
	data = {
		"files": (io.BytesIO(content), "sample.txt")
	}
	response = client.post("/upload/", data=data, content_type="multipart/form-data")

	assert response.status_code in [200]
	
	data = {
		"question": "Which library is used for vector database?"
	}
	response = client.post("/query/", json=data) 

	assert response.status_code == 200
	assert "Error" not in response.json	  
	assert "Answer" in response.json	  
	assert "Question" in response.json	  
	assert "source_chunks" in response.json