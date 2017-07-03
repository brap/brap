from brap.graph import Graph, RegisteredNode


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
        return self._graph.get_node_by_id(id).get_value()

    def set(self, id, value, constructor_dependencies = [], method_dependencies = []):
        """
        Sets a parameter or service by id

        Values are lazy constructed by being baked into functions.
        These functions are how the various features are created, including:
        service(factory), service(class), service(function), factory, parameters

        However, this method does not create a factory.
        """

        # FIXME does not preserve constructed value... perhaps use a memoize pattern
        def class_value():
            instance = value(*constructor_dependencies)
            for method_map in method_dependencies:
                method = getattr(instance, method_map[0])
                method(*method_map[1])

            return instance

        def fn_value():
            result = value(*constructor_dependencies)
            return result

        def other_value():
            return value

        edges = constructor_dependencies + [dep[1] for dep in  method_dependencies]

        # check if value is class
        if isinstance(value, type):
            self._graph.add_node(RegisteredNode(id, edges, class_value))
            return self

        # check if value is function
        if callable(value):
            self._graph.add_node(RegisteredNode(id, edges, fn_value))
            return self

        # value is something else
        self._graph.add_node(RegisteredNode(id, edges, other_value))
        return self


    def factory(self, id, callable_service, constructor_dependencies = [], method_dependencies = []):
        """
        Marks a callable as being a factory service.
        """

        if not isinstance(callable_service, type):
            raise Exception('FIXME better exception')


        # FIXME duplicate logic with set()
        edges = constructor_dependencies + [dep[1] for dep in  method_dependencies]

        # FIXME does not preserve constructed value... And that should be fine here?
        def factory_class_value():
            instance = callable_service(*constructor_dependencies)
            for method_map in method_dependencies:
                method = getattr(instance, method_map[0])
                method(*method_map[1])

            return instance

        self._graph.add_node(RegisteredNode(id, edges, factory_class_value))
        return self

    def registerProvider(self, provider):
        """
        Registers a service provider.
        """
        if not isinstance(provider , ProviderInterface):
            raise ValueError('Provider must extend ProviderInterface')

        provider.register(self)

        return self


class ProviderInterface(object):
    def register(self, container):
        raise NotImplementedError('Providers must have a register method')
