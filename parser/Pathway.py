import networkx as nx

class Pathway():

    def __init__(self):
        self.g = nx.DiGraph()       # the graph 
        self.name = ''              # KEGG identifier of pathway map
        self.org = ''               # organism type
        self.number = ''            # pathway map identification number
        self.title = ''             # title of pathway map

    def set_name(self, name):
        self.name = name

    def set_org(self, org):
        self.org = org

    def set_number(self, number):
        self.number = number

    def set_title(self, title):
        self.title = title

    def add_node(self, n, data = None):
        networkx.DiGraph.add_node(self, n, data)

    def get_genes(self):
        """
        return a subgraph composed only by the genes
        >>> p = KeggPathway()
        >>> p.add_node('gene1', data={'type': 'gene'})
        >>> p.add_node('compound1', data={'type': 'compound'})
        >>> subgraph = p.get_genes()
        >>> print subgraph.nodes()
        ['gene1']
        """
#        subgraph = self.subgraph([node for node in self.nodes() if self.node[node]['type'] == 'gene'])
        genes = []
        labels = {}
        for n in self.nodes():
            if self.node[n]['type'] == 'gene':
                genes.append(n)
                labels[n] = self.node[n]
#            else:
#                self.labels.pop(node)
        subgraph = self.subgraph(genes)
        subgraph.title = self.title + ' (genes)'
        subgraph.labels = labels
        return subgraph

    def neighbors_labels(self, node):
        """
        like networkx.graph.neighbours, but returns gene label
        >>> p = KeggPathway()
        >>> p.add_node(1, data={'label': 'gene1'})
        >>> p.add_node(2, data={'label': 'gene2'})
        >>> p.add_edge(1, 2)
        >>> p.neighbors(1)
        [2]
        >>> p.neighbors_labels(1)
        {'gene1': ['gene2']}
        """
        neighbours = self.neighbors(node)
        labels = [self.node[n]['label'] for n in neighbours]
        return {self.node[node]['label']: labels}


    def __repr__(self):
        return self.title + ' pathway'
