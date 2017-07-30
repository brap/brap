import itertools


def extract_edges_from_callable(fn):
    """
    This takes args and kwargs provided, and returns the names of the strings
    assigned. If a string is not provided for a value, an exception is raised.

    This is how we extract the edges provided in the brap call lambdas.
    """

    def extractor(*args, **kwargs):
        """
        Because I don't think this technique is common in python...

        Service constructors were defined as:
            lambda c: c('a')

        In this function:
            fn = lambda c: c('a')
            fn(anything)  # Results in anything('a')

        Here we provide a function which returns all args/kwargs
            fn(extractor)  # ["a"]

        This isn't voodoo, it's just treating a function's call if it is data.
        """
        return list(args) + list(kwargs.values())

    edges = fn(extractor)

    for edge in edges:
        if not isinstance(edge, str):
            raise ValueError('Provided edge "{}" is not a string'.format(edge))

    return list(edges)


class Registration(object):
    """
    Registration remembers how nodes for a graph are registered, and can
    determine things such as what the edges it was registered with are

    This is how a pre-compiled graph can dig into the way a node was registered
    """

    def __init__(self, node_id):
        self._node_id = node_id

    def get_id(self):
        return self._node_id

    def get_edges(self):
        raise Exception("Edges only computable for concrete registration")


class ParameterRegistration(Registration):
    def __init__(self, node_id, value):
        super().__init__(node_id)
        self._value = value

    def get_value(self):
        return self._value

    def get_edges(self):
        return []


class FunctionRegistration(Registration):
    def __init__(self, node_id, function_reference, call=lambda c: ()):
        super().__init__(node_id)
        self._function_reference = function_reference
        self._call = call

    def get_function_reference(self):
        return self._function_reference

    def get_callable(self):
        return self._call

    def get_edges(self):
        return extract_edges_from_callable(self._call)


# TODO perhaps prohibit extension with final?
class ClassRegistration(Registration):
    def __init__(
            self,
            node_id,
            class_reference,
            constructor_call=lambda c: (),
            method_calls=[]):

        super().__init__(node_id)
        self._class_reference = class_reference
        self._constructor_call = constructor_call
        self._method_calls = method_calls

    def get_edges(self):
        method_edges = [extract_edges_from_callable(
            dep[1]) for dep in self._method_calls]
        edges = list(extract_edges_from_callable(
            self._constructor_call)) + list(itertools.chain(*method_edges))

        return edges

    def get_class_reference(self):
        return self._class_reference

    def get_constructor_call(self):
        return self._constructor_call

    def get_method_calls(self):
        return self._method_calls
