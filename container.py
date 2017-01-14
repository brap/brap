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
        self._container = {}  # The container map
        self._values = {}
        self._factories = set()

    def get(self, id):
        """
        Gets a parameter or the closure defining an object.
        """
        if not self._container[id]:
            raise ValueError('Identifier "{}" is not defined.'.format(id))

        return self._container[id]

    def set(self, id, value):
        """
        """
        if self._container[id]:
            raise ValueError('Identifier "{}" is already defined.'.format(id))

        self._container[id] = value

        return self._container[id]

    def factory(self, id, callable_service):
        """
        Marks a callable as being a factory service.
        """
        if not callable(callable_service):
            raise ValueError('Service definition is not callable.')

        self._factories[id] = callable_service

        return self.get()

    def register(self, provider, values):
        """
        Registers a service provider.
        """
        # TODO check for instance of ProviderInterface
        provider.register(self)

        for key, value in value_map:
            self.setattr(key, value)

        return self


class ProviderInterface(object):
    def register(self, container):
        raise NotImplementedError('Providers must have a register method')
