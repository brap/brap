class Graph(object):
    """
    Perhaps I could make Brap2 use Brap1 to avoid this hard dependency?
    """
    def __init__(self):
        self._nodeMap = {}

    def _create_unregistered_edge_node(self, node_id):
        return UnregisteredNode(node_id)  # Unfortunate hard dependency

    def add_node(self, node):
        if not isinstance(node, Node):
            raise ValueError('Provided object {} is not a Node'.format(node.__class__.__name__))  # Fixme more specific exception type

        # Only add new nodes. Only replace UnregisteredNode
        if node.get_id() in self._nodeMap:
            if not isinstance(node, UnregisteredNode):
                raise ValueError('Identifier "{}" is already in graph.'.format(node.get_id()))

        # Register undefined edges
        for edge_node_id in node.get_edges():
            if edge_node_id not in self._nodeMap:
                unregistered_node = self._create_unregistered_edge_node(edge_node_id)
                self.add_node(unregistered_node)

        # Put node in map
        self._nodeMap[node.get_id()] = node

    def get_node_by_id(self, node_id):
        return self._nodeMap[node_id]  # TODO if not present, exception

    def get_dependency_lists(self):  # I may only have this for the sake of testing. TBD.
        return [(node_id, self.get_node_by_id(node_id).get_edges()) for node_id in self._nodeMap]


class Node(object):
    """
    Abstract base node
    """
    def __init__(self, node_id, edges=[]):
        self._id = node_id
        self._edges = edges

    def get_id(self):
        return self._id

    def get_edges(self):
        return self._edges


class UnregisteredNode(Node):
    """
    Registers edges that were mentioned but not directly registered
    """
    pass


class ServiceNode(Node):  # TODO think about renaming to RegisteredNode
    """
    Registers nodes that were deliberate
    """
    pass
