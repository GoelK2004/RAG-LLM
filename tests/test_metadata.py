def test_metadata_show(client):
	"""
	Test the metadata route of the project
	"""
	
	response = client.get("/metadata/")
	
	assert response.status_code in [200]
	assert isinstance(response.json, list)