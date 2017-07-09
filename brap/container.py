from functools import partial

from brap.graph import Graph

from brap.node_registrations import (
    FunctionRegistration,
    ClassRegistration,
    ParameterRegistration,
)


class Container(object):
    """
    The main brap container

    Stores parameters and callables
    """

    def __init__(self, graph=Graph()):
        """
        Instantiate the container.
        """
        self._graph = graph

    def get(self, id):
        """
        Gets a parameter or the closure defining an object.
        """
        # fixme give graph a method to find value by ID
        return self._graph.get_node_by_id(id).get_value()

    def merge(self, subordinate_container):
        if not isinstance(subordinate_container, Container):
            raise Exception(
                "Container is expected to only merge with a Container.")

        self._graph.merge(subordinate_container._graph)

    def set(self,
            id,
            value,
            constructor_dependencies=lambda c: c(),
            method_dependencies=[]):
        """
        Sets a parameter or service by id

        Values are lazy constructed by being baked into functions.
        These functions are how the various features are created, including:
        service(factory), service(class), service(function), factory,
        parameters

        However, this method does not create a factory.
        """

        # check if value is class
        if isinstance(value, type):
            registration = ClassRegistration(
                id, value, constructor_dependencies, method_dependencies)
            self._graph.register(registration)
            return self

        # check if value is function
        if callable(value):
            registration = FunctionRegistration(
                id, value, constructor_dependencies)
            self._graph.register(registration)
            return self

        # when value is something else
        registration = ParameterRegistration(id, value)
        self._graph.register(registration)
        return self

    def factory(
            self,
            id,
            callable_factory,
            constructor_dependencies=lambda c: c(),
            method_dependencies=[]):
        """
        Marks a callable as being a factory service.
        """

        if not isinstance(callable_factory, type):
            raise Exception('FIXME better exception')

        # FIXME this is totally broken, how do I want to get a new instance?`
        registration = ClassRegistration(
            id, value, constructor_dependencies, method_dependencies)
        self._graph.register(registration)
        return self
