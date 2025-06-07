import os
from flask import Flask
from flask_cors import CORS

from app.api.upload import upload_blueprint
from app.api.metadata import metadata_blueprint
from app.api.query import query_blueprint
from app.db.database import init_metadata_db
from app.utils.constants import VECTOR_DB_PATH

def create_app():
	app = Flask(__name__)
	CORS(app)

	app.register_blueprint(upload_blueprint, url_prefix="/upload")
	app.register_blueprint(metadata_blueprint, url_prefix="/metadata")
	app.register_blueprint(query_blueprint, url_prefix="/query")

	init_metadata_db()
	if not os.path.exists(VECTOR_DB_PATH.split('/')[0]):
		os.mkdir(VECTOR_DB_PATH.split('/')[0])

	return app

if __name__ == "__main__":
	app = create_app()
	app.run(host="0.0.0.0", port=5000)
