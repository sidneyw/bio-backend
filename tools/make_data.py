import os
import json
from pymongo import MongoClient
from bioservices.kegg import KEGG

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
                "id": relation["entry1"] + relation["entry1"],
                "source": relation["entry1"],
                "target": relation["entry2"],
            }
        })

    return { "nodes": nodes, "edges": edges }

if __name__ == "__main__":
    mongo = MongoClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017/"))
    db = mongo["pathi"]

    kegg = KEGG()

    if not os.path.exists("data"):
        os.mkdir("data")

    res = kegg.list("pathway", organism="hsa")
    pathways = [x.split()[0] for x in res.strip().split("\n")]

    print("Fetching Pathway Data")
    all_pathway_data = map(lambda x: kegg.parse_kgml_pathway(x), pathways)

    print("Writing Out Pathway Data")
    for ind, response in enumerate(all_pathway_data):
        filePath = os.path.join("data", "%s.json" % pathways[ind])
        print(filePath)

        output = formatPathway(response)
        with open(filePath, "w") as f:
            json.dump(output, f, indent=2)
