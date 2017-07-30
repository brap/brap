from functools import partial

from brap.graph import Graph
from copy import deepcopy

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

    def __init__(self, graph=None):
        """
        Instantiate the container.
        """
        if graph:
            self._graph = graph
        else:
            self._graph = Graph()

    def get(self, node_id):
        """
        Gets a parameter or the closure defining an object.
        """
        return self._graph.get_value_by_node_id(node_id)

    def merge(self, subordinate_container):
        if not isinstance(subordinate_container, Container):
            raise Exception(
                "Container is expected to only merge with a Container.")

        self._graph.merge(subordinate_container.get_graph_clone())

    def get_graph_clone(self):
        return deepcopy(self._graph)

    def set(self,
            node_id,
            value,
            constructor_dependencies=lambda c: c(),
            method_dependencies=[]):

        # check if value is class
        if isinstance(value, type):
            registration = ClassRegistration(
                node_id, value, constructor_dependencies, method_dependencies)
            self._graph.register(registration)
            return self

        # check if value is function
        if callable(value):
            registration = FunctionRegistration(
                node_id, value, constructor_dependencies)
            self._graph.register(registration)
            return self

        # when value is something else
        registration = ParameterRegistration(node_id, value)
        self._graph.register(registration)
        return self

    def use_compiler(self, compiler):
        compiler.compile(self._graph)
