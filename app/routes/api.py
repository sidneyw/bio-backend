""" ROUTES """
from pymongo import MongoClient
from flask import Blueprint, jsonify, request
import json
import os

blueprint = Blueprint('/api', __name__, url_prefix='/api')

mongo = MongoClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017/"))
db = mongo["pathi"]


def formatPathway(pathwayDict):
    nodes = [];
    edges = [];

    for entry in pathwayDict["entries"]:
        if entry["type"] == "compound":
            shape = "triangle"
        elif entry["type"] == "ortholog":
            shape = "ellipse"
        else:
            shape = "rectangle"

        nodes.append({
            "data": {
                "id": entry["id"],
                "name": entry["name"],
                "shape": shape,
            }
        })

    for relation in pathwayDict["relations"]:
        edges.append({
            "data": {
                "id": relation["entry1"] + relation["entry2"],
                "source": relation["entry1"],
                "target": relation["entry2"],
            }
        })

    return { "nodes": nodes, "edges": edges }

with open("./file_for_playing.json", "r") as f:
    pathwayData = json.load(f)
    print(pathwayData)

sampleData = formatPathway(pathwayData)

# =======================
# Routes
# =======================
@blueprint.route('/test', methods=['POST'])
def test():
    request_data = request.json
    return jsonify({
        "received": request_data,
    })

@blueprint.route("/sample", methods=["GET"])
def sample():
    response = jsonify(sampleData)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
