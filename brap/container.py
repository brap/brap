from brap.graph import Graph, ServiceNode


class Container(object):
    """
    The main brap container

    Stores parameters and callables
    """

    def __init__(self):
        """
        Instantiate the container.
        Objects and parameters can be passed as argument to the constructor.
        value_map are initial parameters or objects
        """
        self._graph = Graph()  # Graph to detect design flaws. Only mirrors structure, doesn't do anything useful.

    def get(self, id):
        """
        Gets a parameter or the closure defining an object.
        """
        return self._graph.get_node_by_id(id)

    def set(self, id, value):
        """
        Sets a parameter or service by id
        """
        if id in self._raw:
            raise ValueError('Identifier "{}" is already defined.'.format(id))

        self._raw[id] = value

        return self

# TODO
#   def factory(self, id, callable_service):
#       """
#       Marks a callable as being a factory service.
#       """
#       if id in self._raw:
#           raise ValueError('Identifier "{}" is already defined.'.format(id))

#       if id in self._factories:
#           raise ValueError('Identifier "{}" is already defined, but something is very wrong because it is not in _raw.'.format(id))

#       if not callable(callable_service):
#           raise ValueError('Factory definition must be callable.')

#       self._raw[id] = callable_service
#       self._factories[id] = callable_service

#       return self

# TODO
#   def registerProvider(self, provider):
#       """
#       Registers a service provider.
#       """
#       if not isinstance(provider , ProviderInterface):
#           raise ValueError('Provider must extend ProviderInterface')

#       provider.register(self)

#       return self


class ProviderInterface(object):
    def register(self, container):
        raise NotImplementedError('Providers must have a register method')
