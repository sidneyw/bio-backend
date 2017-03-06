""" ROUTES """
from pymongo import MongoClient
from flask import Blueprint, jsonify, request
import os

blueprint = Blueprint('/api', __name__, url_prefix='/api')

mongo = MongoClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017/"))
db = mongo["pathi"]

@blueprint.route('/test', methods=['POST'])
def test():
    request_data = request.json
    return jsonify({
        "received": request_data,
    })
