from brap.nodes import RegisteredNode
from brap.node_registrations import Registration

class Graph(object):
    def __init__(self):
        self._nodeMap = {}

    def add_node(self, registration):
        if not isinstance(registration, Registration):
            raise ValueError('Provided object {} is not a Registration'.format(
                registration.__class__.__name__))  # Fixme more specific exception type

        # Only add new nodes. Only replace UnregisteredNode
        if registration.get_id() in self._nodeMap:
            if not isinstance(self._nodeMap[registration.get_id()], UnregisteredNode):
                raise ValueError(
                    'Identifier "{}" is already in graph.'.format(registration.get_id()))

        registered_node = RegisteredNode(registration)

        # Put node in map
        self._nodeMap[registered_node.get_id()] = registered_node

    def get_node_by_id(self, node_id):
        return self._nodeMap[node_id]  # TODO if not present, exception

    def get_nodes(self):
        return self._nodeMap
