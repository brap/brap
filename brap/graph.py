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
            if not isinstance(self._nodeMap[node.get_id()], UnregisteredNode):
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

    def get_nodes(self):
        return self._nodeMap

    def get_dependency_lists(self):  # FIXME I may only have this for the sake of testing. TBD.
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
    def get_value(self):
        raise Exception('Unregistered node "{}" called by Brap Container. Unregistered nodes never have values.'.format(self._id))

class RegisteredNode(Node):  # TODO think about renaming to RegisteredNode
    """
    Registers nodes that were deliberate
    """
    def __init__(self, node_id, edges=[], value=None):
        super().__init__(node_id, edges)
        self._value = value

    def get_value(self):
        return self._value()


class NodeVisitorDecorator(object):
    def __init__(self, node):
        self._node = node
        self._weight = 0
        self._node_id = node.get_id()

    def get_weight(self):
        return self._weight

    def increment(self):
        self._weight += 1

    def decrement(self):
        self._weight -= 1

    def get_id(self):
        return self._node_id

    def get_node(self):
        return self._node


class GraphAnalyzer():
    def __init__(self, graph):
        self._graph = graph;

        self._circular_dependencies = []
        self._sorted_nodes = []

        self._topological_sort()

    def get_circular_dependencies(self):
        return self._circular_dependencies

    def get_sorted_nodes(self):
        return self._sorted_nodes

    def get_unregistered_nodes(self):
        nodeMap = self._graph.get_nodes()
        return [nodeMap[node] for node in nodeMap if isinstance(nodeMap[node], UnregisteredNode)]

    def _topological_sort(self):
        """
        Kahn's algorithm for Topological Sorting
        - Finds cycles in graph
        - Computes dependency weight
        """
        sorted_graph = []
        nodeMap = self._graph.get_nodes()

        # FIXME demeter's law
        nodes = [NodeVisitorDecorator(nodeMap[node]) for node in nodeMap]

        def get_pointers_for_edge_nodes(visitor_decorated_node):
            edges = []
            edge_ids = visitor_decorated_node.get_node().get_edges()
            for node in nodes:
                if node.get_id() in edge_ids:
                    edges.append(node)

            return edges

        # Each node is initially weighted with the number of immediate dependencies
        for node in nodes:
            for edge in get_pointers_for_edge_nodes(node):
                edge.increment()

        # Start with a list of nodes who have no dependents
        resolved = [node for node in nodes if node.get_weight() == 0]

        while resolved:
            node = resolved.pop()
            sorted_graph.append(node)

            for edge in get_pointers_for_edge_nodes(node):
                edge.decrement()
                if edge.get_weight() == 0:
                    resolved.append(edge)

        self._circular_dependencies = [node.get_node() for node in nodes if node.get_weight() > 0]

        self._sorted_nodes = reversed([node.get_node() for node in sorted_graph])
