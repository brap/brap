from brap.nodes import RegisteredNode, UnregisteredNode
from brap.node_registrations import Registration

class Graph(object):
    def __init__(self):
        self._nodeMap = {}

    def _is_node_reserved(self, node):
        return node.get_id() in self._nodeMap

    def _add_node(self, node):
        """
        Adds node if name is available or pre-existing node is unregistered
        returns True if added
        returns False if not added
        """
        if self._is_node_reserved(node):
            if not isinstance(self._nodeMap[node.get_id()], UnregisteredNode):
                return False

        # Put node in map
        self._nodeMap[node.get_id()] = node
        return True

    def register(self, registration):
        """
        """
        if not isinstance(registration, Registration):
            raise ValueError('Provided object {} is not a Registration'.format(
                registration.__class__.__name__))

        registered_node = RegisteredNode(registration)

        is_added = self._add_node(registered_node)

        if not is_added:
            raise ValueError('Cannot register a node named "{}" which has already been registered'.format(registered_node.get_id()))

    def get_node_by_id(self, node_id):
        return self._nodeMap[node_id]

    def get_nodes(self):
        return self._nodeMap

    def merge(self, subordinate_graph):
        """
        merge rules:
        00 + 00 == 00    00 + 0B == 0B
        0A + 00 == 0A    0A + 0B == 0A
        A0 + 00 == A0    A0 + 0B == AB
        AA + 00 == AA    AA + 0B == AB

        00 + B0 == B0    00 + BB == BB
        0A + B0 == BA    0A + BB == BA
        A0 + B0 == A0    A0 + BB == AB
        AA + B0 == AA    AA + BB == AA
        """
        if not isinstance(subordinate_graph, Graph):
            raise Exception("Graph is expected to only merge with a Graph.")

        subordinate_nodes = subordinate_graph.get_nodes()

        merge_results = []
        for node_id in subordinate_nodes:
            node = subordinate_nodes[node_id]
            merge_results.append((
                node.get_id(),
                self._add_node(node)
            ))

        # TODO perhaps throw exception if merge was unsuccessful
        return merge_results
