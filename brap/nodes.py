class Node(object):
    """
    Abstract base node
    """

    def get_id(self):
        raise Exception('Abstract method called.')

    def get_edges(self):
        raise Exception('Abstract method called.')


class RegisteredNode(Node):
    """
    Registers nodes that were deliberate
    """

   # FIXME edges can be put into registration object instead of graph or injected here.
    def __init__(self, registration=None):
        self._registration = registration  # TODO ensure is instance of registration
        self._tags = []

    def get_id(self):
        return self._registration.get_id()

    def get_value(self):
        raise Exception(
            'Registered node "{}" was requested without being compiled.'.format(self._id))

    def get_edges(self):
        return self._registration.get_edges()

    def set_tags(self, tags):
        self._tags = tags

    def get_tags(self):
        return self._tags

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

