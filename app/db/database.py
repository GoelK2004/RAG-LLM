import sqlite3
import os
from datetime import datetime

from app.utils.constants import DB_FILE

def init_metadata_db():
	"""
	Creates metadata db if it doesnt exist.
	"""
	
	if not os.path.exists(DB_FILE.split('/')[0]):
		os.mkdir(DB_FILE.split('/')[0])
	
	conn = sqlite3.connect(DB_FILE)
	cursor = conn.cursor()

	cursor.execute("""
		CREATE TABLE IF NOT EXISTS documents (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			filename TEXT NOT NULL,
			page_count INTEGER NOT NULL,
			chunk_count INTEGER NOT NULL,
			upload_time TEXT NOT NULL		
		)
	""")

	conn.commit()
	conn.close()

def store_document_metadata(file_name: str, page_count: int, chunks_count: int):
	"""
	Inserts new record in the metadata table
	Arguments:
		file_name: Name of the file
		chunks_count: Total number of chunks generated
	"""
	conn = sqlite3.connect(DB_FILE)
	cursor = conn.cursor()

	cursor.execute("""
		INSERT INTO documents (filename, page_count, chunk_count, upload_time) VALUES (?, ?, ?, ?)
	""",
	(file_name, page_count, chunks_count, datetime.now().isoformat())
	)

	conn.commit()
	conn.close()

def get_all_metadata():
	"""
	Fetches all document records from the database
	"""

	conn = sqlite3.connect(DB_FILE)
	cursor = conn.cursor()

	cursor.execute("""
		SELECT filename, page_count, chunk_count, upload_time FROM documents
	""")

	rows = cursor.fetchall()

	return [{f"Filename":row[0], f"Pages": row[1], f"Chunks": row[2], f"Time":row[3]} for row in rows]