import copy

from brap.compilers.compiler import Compiler
from brap.nodes import Node


class EagerDependencyInjectionCompiler(object):
    def __init__(self, service_node, function_node, parameter_node):
        pass

    def compile(self, graph):
        nodes = graph.get_nodes()

        for node_id in nodes:
            eager_node = self.transform_registered_node(nodes[node_id])
            pass

class EagerNodeFactory():
    def from_registration():
        raise Exception('This is a base class, do not actually use it.')

class CallableEagerNodeFactory(EagerNodeFactory):
    def hydrate_callable_with_container(container, callable_function, parameter_lambda):
        """
        args and kwargs intentionally not *args and **kwargs
        """

        def extract_kwargs_dict(*args, **kwargs):
            return kwargs

        def extract_args_list(*args, **kwargs):
            return list(args)

        args = parameter_lambda(extract_args_list)
        kwargs = parameter_lambda(extract_kwargs_dict)

        arg_list = [container.get(id) for id in list(args)]

        kwarg_map = {}

        for kwarg in kwargs:
            kwarg_map[kwarg] = container.get(kwargs[kwarg])

        return callable_function(*arg_list, **kwarg_map)

class ServiceEagerNodeFactory(CallableEagerNodeFactory):
    def from_registration(registration):
        instance = hydrate_callable_with_container(self, value, constructor_dependencies)
        for method_map in method_dependencies:
            method = getattr(instance, method_map[0])
            hydrate_callable_with_container(self, method, method_map[1])

        id = 'FIXME_inst'
        return ServiceEagerNode(id, value)

class FunctionEagerNodeFactory(CallableEagerNodeFactory):
    def from_registration(registration):
        func = hydrate_callable_with_container(self, value, constructor_dependencies)

        id = 'FIXME_func'
        return ServiceEagerNode(id, func)

class ParameterEagerNodeFactory(EagerNode):
    def from_registration(registration):
        id = 'FIXME_param'
        value = 'fixme value'
        return ServiceEagerNode(id, value)

class EagerNode(Node):
    def __init__(self):
        self._id = None

    def get_id(self):
        return self._id

    def get_value(self):
        raise Exception('Abstract Eager Nodes do not have values')


class ServiceEagerNode(EagerNode):
    def __init__(self, id, instance):
        self._id = id
        self._instance = instance

    def get_value(self):
        return self._instance

class ParameterEagerNode(EagerNode):
    def __init__(self, id, value):
        self._id = id
        self._value = value

    def get_value(self):
        return self._value


class FunctionEagerNode(EagerNode):
    def __init__(self, id, func):
        self._id = id
        self._func = func

    def get_value(self):
        return self._func


# TODO more meta-level, not sure how to define this one. yet.
class FactoryEagerNode(EagerNode):
    def __init__(self):
        self._id = None
        self._instance = None

    def get_value(self):
        raise Exception('TODO')
