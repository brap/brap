import copy

from brap.compilers.compiler import Compiler


class NodeVisitor(object):
    def __init__(self, node):
        self._node = node
        self._weight = 0

    def get_weight(self):
        return self._weight

    def increment(self):
        self._weight += 1

    def decrement(self):
        self._weight -= 1

    def get_id(self):
        return self._node.get_id()

    def get_node(self):
        return self._node


class GraphSorter(Compiler):
    def __init__(self, graph):

        # I refuse to accept a side-effect here
        self._graph = copy.deepcopy(graph)

        self._circular_dependencies = []
        self._sorted_nodes = []

        self._topological_sort()

    def get_circular_dependencies(self):
        return self._circular_dependencies

    def get_sorted_nodes(self):
        return self._sorted_nodes

    def _topological_sort(self):
        """
        Kahn's algorithm for Topological Sorting
        - Finds cycles in graph
        - Computes dependency weight
        """
        sorted_graph = []
        node_map = self._graph.get_nodes()

        nodes = [NodeVisitor(node_map[node]) for node in node_map]

        def get_pointers_for_edge_nodes(visitor_decorated_node):
            edges = []
            edge_ids = visitor_decorated_node.get_node().get_edges()
            for node in nodes:
                if node.get_id() in edge_ids:
                    edges.append(node)

            return edges

        # node is initially weighted with the number of immediate dependencies
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

        self._circular_dependencies = [
            node.get_node() for node in nodes if node.get_weight() > 0]

        self._sorted_nodes = list(reversed(
            [node.get_node() for node in sorted_graph]))


class CircularDependencyCompiler(Compiler):
    # TODO think about how to plug analytics into here
    def __init__(self, graph_sorter=GraphSorter):
        self._graph_sorter = graph_sorter
        self._sorted_graph = None

    def compile(self, graph):
        self._sorted_graph = self._graph_sorter(graph)

        if self._sorted_graph.get_circular_dependencies() != []:
            raise Exception('Found circular dependencies: {}'.format(
                self._sorted_graph.get_circular_dependencies()
            ))
