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
    pid = ""
    nodes = [];
    edges = [];

    for entry in pathwayDict["entries"]:
        if entry["type"] == "pway":
            pid = entry["name"]
            continue
        if entry["type"] != "ortholog": # orthologs don't have edges in KEGG's maps

            nodes.append({
                "data": {
                    "id": entry["id"],
                    "db_name": entry["name"],
                    "type": entry["type"],
                    "name": entry["gene_names"],
                    "db_link": entry["link"],
                    "x_coord": entry["x_coord"],
                    "y_coord": entry["y_coord"]
                },
                "position": {
                    'x': (int(entry["x_coord"])*3),
                    'y': (int(entry["y_coord"])*2)
                }
        })

    for relation in pathwayDict["relations"]:
        edges.append({
            "data": {
                "id": "rel" + relation["entry1"] + "to" + relation["entry2"],
                "source": relation["entry1"],
                "target": relation["entry2"],
                "type": "rel",
                "link": relation["link"],
                "value": relation["value"],
                "subtype": relation["name"]
            }
        })

    for reaction in pathwayDict["reactions"]:
        for subst in reaction["substrates"]:
            for prod in reaction["products"]:
                edges.append({
                    "data": {
                        "id": "react" + subst["id"] + "to" + prod["id"],
                        "source": subst["id"],
                        "target": prod["id"],
                        "type": "reaction",
                        "substrate": subst["name"],
                        "product": prod["name"],
                        "subtype": reaction["type"],
                        "name": reaction["name"],
                        "value": reaction["value"]
                    }
                })

    return { "id": pid, "nodes": nodes, "edges": edges }

# with open("./file_for_playing.json", "r") as f:
    # pathwayData = json.load(f)

# sampleData = formatPathway(pathwayData)

# =======================
# Routes
# =======================
@blueprint.route("/sample", methods=["GET"])
def sample():
    print(request.args)
    return jsonify(sampleData)


@blueprint.route("/pathway", methods=["GET"])
def pathway():
    ## Modified from: https://pythonhosted.org/bioservices/_modules/bioservices/kegg.html#KEGG.parse_kgml_pathway
    pathway_name = request.values.get("id", "None")

    output = {'relations':[], 'entries':[], 'reactions':[]}
    res1 = kegg.easyXML(kegg.get(pathway_name, "kgml"))

    entries = [x for x in res1.findAll("entry")]
    for entry in entries:
        if request.values.get("id") == entry.get("id"): ## We added this
            output['entries'].append({
                'id': entry.get("id"),
                'name': entry.get("name"),
                'type': "pway",
                'link': entry.get("link"),
                'gene_names': entry.find("graphics").get("name"),
                'x_coord': entry.find("graphics").get("x"),
                'y_coord': entry.find("graphics").get("y")
            })
            continue
        output['entries'].append({
            'id': entry.get("id"),
            'name': entry.get("name"),
            'type': entry.get("type"),
            'link': entry.get("link"),
            'gene_names': entry.find("graphics").get("name"),
            ## This is what we added: Accessing other parts of kgml file
            'x_coord': entry.find("graphics").get("x"),
            'y_coord': entry.find("graphics").get("y")
        })

    relations = [(x.get("entry1"), x.get("entry2"), x.get("type")) for x in res1.findAll("relation")]
    subtypes = [x.findAll("subtype") for x in res1.findAll("relation")]

    assert len(subtypes) == len(relations)

    for relation, subtype in zip(relations, subtypes):
        if len(subtype)==0: # nothing to do with the species ??? TODO
            pass
        else:
            for this in subtype:
                value = this.get("value")
                name = this.get("name")
                output['relations'].append({
                    'entry1':relation[0],
                    'entry2':relation[1],
                    'link':relation[2],
                   'value':value,
                    'name':name})

    ## We also added the reactions stuff
    reactions = [x for x in res1.findAll("reaction")]

    for reaction in reactions:
        subs = reaction.findAll("substrate")
        substrates = []
        for sub in subs:
            substrates.append({
                'id': sub.get("id"),
                'name': sub.get("name")
            })
        prods = reaction.findAll("product")
        products = []
        for prod in prods:
            products.append({
                'id': prod.get("id"),
                'name': prod.get("name")
            })
        reaction = { 'value': reaction.get("id"),
            'name': reaction.get("name"),
            'type': reaction.get("type"),
            'substrates': substrates,
            'products': products}
        output['reactions'].append(reaction)

    # we need to map back to KEgg IDs...
    # data = output


    # data = kegg.parse_kgml_pathway(pathway_name)
    return jsonify(formatPathway(output))
    # return jsonify(formatPathway(data))

@blueprint.route("/list", methods=["GET"])
def list():
    res = kegg.list("pathway", organism="hsa")
    print(res)
    # pathways = [x.split()[0] for x in res.strip().split("\n")]

    pathways = []

    for pathway in res.strip().split("\n"):
        splitPath = pathway.split()
        name = " ".join(splitPath[1:])
        name = name.split("(")[0].strip()

        pathways.append({"id": splitPath[0], "name": name})

    # print("Fetching Pathway Data")
    # all_pathway_data = map(lambda x: kegg.parse_kgml_pathway(x), pathways)

    return jsonify({ "pathways": pathways })

@blueprint.route("/entry", methods=["GET"])
def entry():
    entry = request.values.get("name", "None")
    data = kegg.parse(kegg.get(entry))

    return jsonify({ "entry": entry })
