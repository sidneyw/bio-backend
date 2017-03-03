#!/Users/kyle/cs75-projects/bio-backend/venv/bin/python
import xml.etree.cElementTree as ET
import networkx as nx
import requests

from Pathway import Pathway

def get_kgml():
    base = 'http://rest.kegg.jp/get/'
    path = 'hsa05130/kgml'

    addr = base+path

    r = requests.get(addr)
    assert r.status_code == 200
    return r.text

def parse_pathway(xml_string):

    pathway = Pathway()

    root = ET.fromstring(xml_string)

    pathway.set_name(root.get('name'))         
    pathway.set_org(root.get('org'))
    pathway.set_number(root.get('number'))
    pathway.set_title(root.get('title'))

    return None

    # parse and add nodes
    for entry in tree.getiterator('entry'):
        # get all genes or compounds, and associate ids to names
        logging.debug(entry.get('type') + ' ' + entry.get('id'))

        node_type = entry.get('type')   # can be ('gene', 'compound', 'map'..)


#        if node_type in entriestype:       # something else?
        name = entry.get('name')
        node_id = entry.get('id')
#            if nodes.has_key(id):
#                raise TypeError('over writing a key')
        graphics = entry.find('graphics')
        node_title = graphics.get('name')
        node_x = int(graphics.get('x'))  # Storing the original X and Y to recreate KEGG layout
        node_y = int(graphics.get('y'))
        logging.debug(node_title)

        # some nodes refer to more than a gene, and have a node_title in the form
        # 'nameofthefirstgene...', e.g. 'ALG2...'
        # As a temporary solution (to investigate more), I am just taking the name
        # of the first gene/entity
#        if node_title[-3:] == '...':
#            node_title = node_title[:-3]

        nodes[node_id] = (name, node_title, node_type)
        pathway.labels[node_id] = node_title
        pathway.add_node(node_id, data={'label': node_title, 'type': node_type, 'xy': (node_x, node_y)})
#    logging.debug(nodes)


    # parse and add relations
    for rel in tree.getiterator('relation'):
        e1 = rel.get('entry1')
        e2 = rel.get('entry2')
#        pathway.add_edge(nodes[e1][1], nodes[e2][1])
        pathway.add_edge(e1, e2)
        pathway.relations[e1+'_'+e2] = rel


    # Add reactions to pathway object
    for reaction in tree.getiterator('reaction'):

        id = reaction.get('name')
        substrates = []
        products = []

        for sub in reaction.getiterator('substrate'):
            substrates.append(sub.get('name'))

        for prod in reaction.getiterator('product'):
            products.append(sub.get('name'))

        pathway.reactions[id] = {'reaction': reaction, 'substrates': substrates, 'products': products}

    return tree, pathway, nodes, genes

if __name__ == '__main__':
    data = get_kgml()
    parse_pathway(data)
