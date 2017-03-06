from bioservices.kegg import KEGG
import json
s = KEGG()

data = s.parse(s.get("hsa:83440"))
print(json.dumps(data, indent=2))

res = s.list("pathway", organism="hsa")
pathways = [x.split()[0] for x in res.strip().split("\n")]
print(pathways)

res = s.parse_kgml_pathway("hsa00010")
with open("file_for_playing.json", "w") as f:
    json.dump(res, f, indent=2)
