import fitz
import docx
import io

def extract_text(file_name: str, content: bytes) -> str:
	"""
		Extracts readable text from file formats of .pdf, .docx, .txt files
		Arguments:
			file_name: Name of the file
			content: File content in bytes
		Returns:
			str: Extracted plain text
	"""
	if file_name.lower().endswith(".pdf"):
		try:
			pdf_data = io.BytesIO(content)
			doc = fitz.open(stream=pdf_data, filetype="pdf")
			text = ""
			for page in doc:
				text += page.get_text() + "\n"
			return text.strip()
		except Exception:
			return ""		
	elif file_name.lower().endswith(".docx"):
		try:
			doc_data = docx.Document(io.BytesIO(content))
			return "\n".join([p.text for p in doc_data.paragraphs if p.text]).strip()
		except Exception:
			return ""
	elif file_name.lower().endswith(".txt"):
		try:
			text_data = content.decode("UTF-8").strip()
			return text_data
		except Exception:
			return ""