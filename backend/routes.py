from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401
from .service import get_data

# Load data
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data = get_data()


######################################################################
# RETURN HEALTH OF THE APP
######################################################################
@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200


######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################
@app.route("/count")
def count():
    """Return length of data"""
    if data:
        return jsonify(length=len(data)), 200
    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """Return a list of all pictures"""
    return jsonify(data)


######################################################################
# GET A PICTURE BY ID
######################################################################
@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """Return a specific picture by ID"""
    for picture in data:
        if picture["id"] == id:
            return jsonify(picture)
    abort(404)


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    """Create a new picture"""
    picture = request.get_json()
    
    # Check if picture with this id already exists
    for existing in data:
        if existing["id"] == picture["id"]:
            return {"Message": f"picture with id {picture['id']} already present"}, 302
    
    # Add new picture to data
    data.append(picture)
    return jsonify(picture), 201  # HTTP 201 Created


######################################################################
# UPDATE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """Update an existing picture"""
    picture = request.get_json()
    
    # Find and update the picture
    for existing in data:
        if existing["id"] == id:
            # Update all fields from the request
            existing.update(picture)
            existing["id"] = id  # Ensure ID stays the same (in case it was changed in payload)
            return jsonify(existing), 200
    
    # If not found, return 404
    return {"message": "picture not found"}, 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """Delete a picture by ID"""
    for existing in data:
        if existing["id"] == id:
            data.remove(existing)
            return '', 204  # HTTP_204_NO_CONTENT
    abort(404)