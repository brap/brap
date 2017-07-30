from brap.compilers.compiler import Compiler
from brap.nodes import Node

from brap.compilers.circular_dependency_compiler import GraphSorter

from brap.node_registrations import (
    ParameterRegistration,
    FunctionRegistration,
    ClassRegistration,
)

class EagerNode(Node):
    def __init__(self, node_id):
        self._node_id = node_id

    def get_id(self):
        return self._node_id

    def get_value(self):
        raise Exception('Abstract Eager Nodes do not have values')


class ServiceEagerNode(EagerNode):
    def __init__(self, node_id, instance):
        super().__init__(node_id)
        self._instance = instance

    def get_value(self):
        return self._instance


class ParameterEagerNode(EagerNode):
    def __init__(self, node_id, value):
        super().__init__(node_id)
        self._value = value

    def get_value(self):
        return self._value


class FunctionEagerNode(EagerNode):
    def __init__(self, node_id, func):
        super().__init__(node_id)
        self._func = func

    def get_value(self):
        return self._func


class EagerNodeFactory():
    def from_registration(self):
        raise Exception('This is a base class, do not actually use it.')


class CallableEagerNodeFactory(EagerNodeFactory):
    def hydrate_callable_with_edge_node_map(
            self,
            edge_node_map,
            callable_function,
            parameter_lambda
        ):
        """
        args and kwargs intentionally not *args and **kwargs
        """

        def extract_kwargs_dict(*args, **kwargs):
            return kwargs

        def extract_args_list(*args, **kwargs):
            return list(args)

        args = parameter_lambda(extract_args_list)
        kwargs = parameter_lambda(extract_kwargs_dict)

        arg_list = [edge_node_map[node_id] for node_id in list(args)]

        kwarg_map = {}

        for kwarg in kwargs:
            kwarg_map[kwarg] = edge_node_map[kwargs[kwarg]]

        return callable_function(*arg_list, **kwarg_map)

class ServiceEagerNodeFactory(CallableEagerNodeFactory):
    def from_registration(self, registration, service_map):
        class_reference = registration.get_class_reference()
        constructor_call = registration.get_constructor_call()
        method_calls = registration.get_method_calls()

        instance = self.hydrate_callable_with_edge_node_map(
            service_map,
            class_reference,
            constructor_call
        )

        for method_map in method_calls:
            method = getattr(instance, method_map[0])
            self.hydrate_callable_with_edge_node_map(
                service_map,
                method,
                method_map[1]
            )

        node_id = registration.get_id()
        return ServiceEagerNode(node_id, instance)

class FunctionEagerNodeFactory(CallableEagerNodeFactory):
    def from_registration(self, registration, service_map):
        func = registration.get_function_reference()
        call = registration.get_callable()

        def curry_function():
            return self.hydrate_callable_with_edge_node_map(
                service_map, func, call
            )

        node_id = registration.get_id()
        return FunctionEagerNode(node_id, curry_function)

class ParameterEagerNodeFactory(EagerNodeFactory):
    def from_registration(self, registration):
        node_id = registration.get_id()
        value = registration.get_value()
        return ParameterEagerNode(node_id, value)


class EagerDependencyInjectionCompiler(Compiler):
    def __init__(
            self,
            graph_sorter=GraphSorter,
            service_factory=ServiceEagerNodeFactory(),
            parameter_factory=ParameterEagerNodeFactory(),
            function_factory=FunctionEagerNodeFactory()
        ):
        self._graph_sorter = graph_sorter
        self._sorted_graph = None
        self._service_factory = service_factory
        self._parameter_factory = parameter_factory
        self._function_factory = function_factory

    def compile(self, graph):
        # todo might be interesting to make the graph aware
        # of compiler passes and properties of those, would
        # let me break the depenency on the import of a
        # graph sorter
        sorted_graph = self._graph_sorter(graph)
        uncompiled_sorted_node_ids = sorted_graph.get_sorted_nodes()

        # TODO filter out already eager nodes
        while uncompiled_sorted_node_ids:
            uncompiled_target_node = uncompiled_sorted_node_ids.pop(0)
            target_node_edge_ids = uncompiled_target_node.get_edges()

            edge_service_map = {}
            for node_id in target_node_edge_ids:
                edge_service_map[node_id] = graph.get_node_by_id(node_id).get_value()

            eager_node = self.create_eager_node(uncompiled_target_node, edge_service_map)

            graph.replace_node(eager_node)

        return graph


    def create_eager_node(self, registered_node, edge_service_map):
        registration = registered_node.get_registration()

        if isinstance(registration, ParameterRegistration):
            return self._parameter_factory.from_registration(registration)

        if isinstance(registration, FunctionRegistration):
            return self._function_factory.from_registration(
                registration, edge_service_map
            )

        if isinstance(registration, ClassRegistration):
            return self._service_factory.from_registration(
                registration, edge_service_map
            )
