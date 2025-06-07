from io import BytesIO
import fitz
import docx

def count_pdf_pages(content: bytes) -> int:
	"""
	Counts the total number of pages present in the PDF
	Arguments:
		content: File content in bytes
	Returns:
		int: Total number of pages
	"""
	content = BytesIO(content)
	pdf = fitz.open(stream=content, filetype="pdf")
	return len(pdf)

def est_doc_pages(content: bytes) -> int:
	"""
	Counts the estimated number of pages present in the doc file. Estimates 10 paragraphs per page
	Arguments:
		content: File content in bytes
	Returns:
		int: Estimated number of pages
	"""
	doc = docx.Document(BytesIO(content))
	return max(1, len(doc.paragraphs) // 10)

def est_text_pages(content: bytes) -> int:
	"""
	Counts the estimated number of pages present in the text file. Estimates 30 lines per page
	Arguments:
		content: File content in bytes
	Returns:
		int: Estimated number of pages
	"""
	text = content.decode("UTF-8").strip()
	lines = text.count('\n')
	return max(1, lines // 30)