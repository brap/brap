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

        super().__init__(node_id, edges)
        self._value = value
        self._registration = registration  # TODO ensure is instance of registration
        self._tags = []

    def get_id(self):
        self._registration.get_id()

    def get_value(self):
        raise Exception(
            'Registered node "{}" was requested without being compiled.'.format(self._id))

    def get_edges(self):
        self._registration.get_edges()

    def set_tags(self, tags):
        self._tags = tags

    def get_tags(self, tags):
        return self._tags

