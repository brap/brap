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

    def __init__(self, registration=None):
        # TODO ensure is instance of registration
        self._registration = registration
        self._tags = []

    def get_id(self):
        return self._registration.get_id()

    def get_value(self):
        raise Exception(
            'Node "{}" requested before compiled.'.format(self.get_id()))

    def get_edges(self):
        return self._registration.get_edges()

    def set_tags(self, tags):
        self._tags = tags

    def get_tags(self):
        return self._tags

    def get_edges(self):
        return self._registration.get_edges()

    def get_registration(self):
        return self._registration
