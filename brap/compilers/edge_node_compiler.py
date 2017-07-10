from brap.compilers.compiler import Compiler

from brap.nodes import Node


class UnregisteredNode(Node):
    """
    Nodes that haven't been registered (likely created via an edge)
    """

    def __init__(self, id):
        self._node_id = id

    def get_id(self):
        return self._node_id

    def get_edges(self):
        return []


class EdgeNodeCompiler(Compiler):
    def compile(self, graph):
        nodes = graph.get_nodes()

        edges = []
        for node_id in nodes:
            edges += nodes[node_id].get_edges()

        unregistered_node_ids = [
            edge_id
            for edge_id
            in edges
            if edge_id not in nodes
        ]

        for node_id in set(unregistered_node_ids):
            unregistered_node = UnregisteredNode(node_id)

            is_inserted_successfully = graph.insert_node(unregistered_node)

            if not is_inserted_successfully:
                raise Exception("Unregistered Node could not be inserted")
