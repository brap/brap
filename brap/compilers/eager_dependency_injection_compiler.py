import copy

from brap.compilers.compiler import Compiler
from brap.nodes import Node


class EagerDependencyInjectionCompiler(object):
    def __init__(self):
        pass

    def compile(self, graph):
        nodes = graph.get_nodes()

        for node_id in nodes:
            eager_node = self.transform_registered_node(node)
            pass

    def transform_registered_node(self, node):
        pass

    # TODO maybe this goes into a special home
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


class EagerNode(Node):
    def __init__(self):
        self._id = None

    def get_id(self):
        return self._id

    def get_value(self):
        raise Exception('Abstract Eager Nodes do not have values')

    def get_edges(self):
        raise Exception('Do we care here? FIXME')


class ServiceEagerNode(Node):
    def __init__(self):
        self._id = None
        self._instance = None

    def get_value(self):
        def class_value():
            if id in self._memoized:
                return self._instances[id]

            instance = hydrate_callable_with_container(self, value, constructor_dependencies)
            for method_map in method_dependencies:
                method = getattr(instance, method_map[0])
                hydrate_callable_with_container(self, method, method_map[1])

            self._instances[id] = instance
            return instance


class ParameterEagerNode(Node):
    def __init__(self):
        self._id = None
        self._instance = None

    def get_value(self):
        raise Exception('TODO')


class FunctionEagerNode(Node):
    def __init__(self):
        self._id = None
        self._value = "TODO"
        self._ = "TODO"

    def get_value(self):
        def fn_value():
            #container_constructor_deps = [
            #    self.get(id) for id in extract_edges_from_callable(constructor_dependencies)]
            result = caller(*self._container_constructor_deps)

            return result

        return fn_value


# TODO more meta-level, not sure how to define this one.
class FactoryEagerNode(Node):
    def __init__(self):
        self._id = None
        self._instance = None

    def get_value(self):
        raise Exception('TODO')
