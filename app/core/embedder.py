from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer


def embeddings_from_chunks(chunks: list[str]) -> str:
	"""
	Generates vector embeddings from chunks.
	Arguments:
		chunks: List of string chunks.
	Returns:
		list[list[float]]: List of embedding vectors.
	"""

	model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
	try:
		embeddings = model.encode(chunks, convert_to_numpy=True).tolist()
		return embeddings

	except Exception as e:
		print(f"[Embedding Error] {e}")
		return [[] for _ in chunks]