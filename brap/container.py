import itertools
from functools import partial

from brap.graph import Graph, RegisteredNode


def extract_edges_from_callable(fn):
    """
    This takes args and kwargs provided, and returns the names of the strings
    assigned. If a string is not provided for a value, an exception is raised.

    This is how we extract the edges provided in the brap call lambdas.
    """
    def extractor(*args, **kwargs):
        return list(args) + list(kwargs)

    """
    Because I don't this technique is not common in python...

    Service constructors were defined as:
        lambda c: c('a')
    In this function: 
        fn = lambda c: c('a')
        fn(anything)  # Results in anything('a')

    Here we provide a function which returns all args/kwargs
        fn(extractor)  # ["a"]

    This isn't voodoo, it's just treating a function's call if it is data.
    """
    edges = fn(extractor) 

    for edge in edges:
        if not isinstance(edge, str):
            raise ValueError('Provided edge "{}" is not a string'.format(edge))

    return edges


class Container(object):
    """
    The main brap container

    Stores parameters and callables
    """

    def __init__(self):
        """
        Instantiate the container.
        """
        self._graph = Graph()  # Graph enforces most business rules
        self._memoized = {}  # For values that are services

    def get(self, id):
        """
        Gets a parameter or the closure defining an object.
        """
        return self._graph.get_node_by_id(id).get_value()

    def set(self, id, value, constructor_dependencies=lambda c: c(), method_dependencies=[]):
        """
        Sets a parameter or service by id

        Values are lazy constructed by being baked into functions.
        These functions are how the various features are created, including:
        service(factory), service(class), service(function), factory, parameters

        However, this method does not create a factory.
        """

        def class_value():
            if id in self._memoized:
                return self._memoized[id]

            container_constructor_deps = [self.get(id) for id in extract_edges_from_callable(constructor_dependencies)]
            instance = value(*container_constructor_deps)
            for method_map in method_dependencies:
                method = getattr(instance, method_map[0])
                container_method_deps = [self.get(id) for id in extract_edges_from_callable(method_map[1])]
                method(*container_method_deps)

            self._memoized[id] = instance
            return instance

        def fn_value():
            container_constructor_deps = [
                self.get(id) for id in extract_edges_from_callable(constructor_dependencies)]
            result = value(*container_constructor_deps)

            return result

        def non_callable_value():
            return value

        # check if value is class
        if isinstance(value, type):
            method_edges = [extract_edges_from_callable(dep[1]) for dep in method_dependencies]
            edges = extract_edges_from_callable(constructor_dependencies) + list(itertools.chain(*method_edges))

            self._graph.add_node(RegisteredNode(id, edges, class_value))

            return self

        # check if value is function
        if callable(value):
            edges = extract_edges_from_callable(constructor_dependencies)

            self._graph.add_node(RegisteredNode(id, edges, fn_value))

            return self

        # when value is something else
        edges = []
        self._graph.add_node(RegisteredNode(id, edges, non_callable_value))
        return self

    def factory(self, id, callable_factory, constructor_dependencies=lambda c: c(), method_dependencies=[]):
        """
        Marks a callable as being a factory service.
        """

        if not isinstance(callable_factory, type):
            raise Exception('FIXME better exception')

        # FIXME duplicate logic with set()
        method_edges = [extract_edges_from_callable(dep[1]) for dep in method_dependencies]
        edges = extract_edges_from_callable(constructor_dependencies) + list(itertools.chain(*method_edges))

        def factory_class_value():
            container_constructor_deps = [self.get(id) for id in extract_edges_from_callable(constructor_dependencies)]
            instance = callable_factory(*container_constructor_deps)
            for method_map in method_dependencies:
                method = getattr(instance, method_map[0])
                container_method_deps = [self.get(id) for id in extract_edges_from_callable(method_map[1])]
                method(*container_method_deps)
            return instance

        self._graph.add_node(RegisteredNode(id, edges, factory_class_value))
        return self

    def registerProvider(self, provider):
        """
        Registers a service provider.
        """
        if not isinstance(provider, ProviderInterface):
            raise ValueError('Provider must extend ProviderInterface')

        provider.register(self)

        return self


class ProviderInterface(object):
    def register(self, container):
        raise NotImplementedError('Providers must have a register method')
