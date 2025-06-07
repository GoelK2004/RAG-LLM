from flask import Blueprint, jsonify

from app.db.database import get_all_metadata

metadata_blueprint = Blueprint("metadata", __name__)

@metadata_blueprint.route("/", methods = ["GET"])
def get_metadata():
	"""
	Lists metadata for all uploaded documents
	Returns:
		JSON list of documents metadata records.
	"""

	metadata = get_all_metadata()
	return jsonify(metadata), 200