from brap.compilers.compiler import Compiler


class NodeVisitor(object):
    def __init__(self, node):
        self._node = node
        self._weight = 0
        et_id()

    def get_weight(self):
        return self._weight

    def increment(self):
        self._weight += 1

    def decrement(self):
        self._weight -= 1

    def get_id(self):
        return self._node._node_id

    def get_node(self):
        return self._node


class EdgeNodeCompiler(Compiler):
    def something(self, graph):
        graph.get_nodes()
