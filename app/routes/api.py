from pymongo import MongoClient
from flask import Blueprint, jsonify, request
import json
import os
from bioservices.kegg import KEGG

blueprint = Blueprint('/api', __name__, url_prefix='/api')

kegg = KEGG()
# mongo = MongoClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017/"))
# db = mongo["pathi"]


def formatPathway(pathwayDict):
    nodes = [];
    edges = [];

    for entry in pathwayDict["entries"]:
        nodes.append({
            "data": {
                "id": entry["id"],
                "db_name": entry["name"],
                "type": entry["type"],
                "name": entry["gene_names"],
                "db_link": entry["link"]
            }
        })

    for relation in pathwayDict["relations"]:
        edges.append({
            "data": {
                "id": "rel" + relation["entry1"] + "to" + relation["entry2"],
                "source": relation["entry1"],
                "target": relation["entry2"]
            }
        })

    return { "nodes": nodes, "edges": edges }

with open("./file_for_playing.json", "r") as f:
    pathwayData = json.load(f)

sampleData = formatPathway(pathwayData)

# =======================
# Routes
# =======================
@blueprint.route("/sample", methods=["GET"])
def sample():
    print(request.args)
    return jsonify(sampleData)


@blueprint.route("/pathway", methods=["GET"])
def pathway():
    pathway_name = request.values.get("id", "None")
    data = kegg.parse_kgml_pathway(pathway_name)

    return jsonify(formatPathway(data))

@blueprint.route("/list", methods=["GET"])
def list():
    res = kegg.list("pathway", organism="hsa")
    print(res)
    # pathways = [x.split()[0] for x in res.strip().split("\n")]

    pathways = []

    for pathway in res.strip().split("\n"):
        splitPath = pathway.split()
        name = " ".join(splitPath[1:])
        name = name.split("-")[0].strip()

        pathways.append({"id": splitPath[0], "name": name})

    # print("Fetching Pathway Data")
    # all_pathway_data = map(lambda x: kegg.parse_kgml_pathway(x), pathways)

    return jsonify({ "pathways": pathways })

@blueprint.route("/entry", methods=["GET"])
def entry():
    entry = request.values.get("name", "None")
    data = kegg.parse(kegg.get(entry))

    return jsonify({ "entry": entry })
