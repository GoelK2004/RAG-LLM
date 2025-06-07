from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_doc(text_content: str, chunk_size: int = 500, chunk_overlap: int = 100) -> list[str]:
	"""
	Splits the text into small, manageable and overlapping chunks.
	Arguments:
		text_content: Input text
		chunk_size: Max size of each chunk
		chunk_overlap: Total number of overlapping characters in between chunks.
	Returns:
		list[str]: List of chunks.
	"""
	splitter = RecursiveCharacterTextSplitter(
		chunk_size = chunk_size, 
		chunk_overlap = chunk_overlap, 
		separators=["\n\n", "\n", ".", "?", " ", ""]
	)
	texts = splitter.split_text(text_content)
	return texts