from unittest import TestCase

from tests.fixtures import FixtureService

from brap.nodes import RegisteredNode
from brap.graph import Graph

from brap.compilers.eager_dependency_injection_compiler import (
    ServiceEagerNodeFactory,
    ParameterEagerNodeFactory,
    FunctionEagerNodeFactory,
    EagerDependencyInjectionCompiler,
    ServiceEagerNode,
    ParameterEagerNode,
    FunctionEagerNode
)

from brap.node_registrations import (
    ClassRegistration,
    FunctionRegistration,
    ParameterRegistration
)


class ParameterEagerNodeFactoryTestCase(TestCase):
    def test_from_registration_returns_parameter_eager_node(self):
        factory = ParameterEagerNodeFactory()
        reg = ParameterRegistration('param_reg_id', 'param_value')

        parameter_eager_node = factory.from_registration(reg)
        self.assertEqual(parameter_eager_node.get_value(), 'param_value')


class FunctionEagerNodeFactoryTestCase(TestCase):
    def test_from_registration_returns_function_eager_node(self):
        def function_reference(a1, kwarg1):
            return a1 + kwarg1

        factory = FunctionEagerNodeFactory()
        reg = FunctionRegistration(
            'function_registration_id',
            function_reference,
            lambda c: c('arg1', kwarg1='keywordarg1')
        )

        service_map = {
          'arg1': 1,
          'keywordarg1': 10
        }

        function_eager_node = factory.from_registration(reg, service_map)
        function = function_eager_node.get_value()
        self.assertEqual(function(), 11)  # Because Math


class ServiceEagerNodeFactoryTestCase(TestCase):
    def test_from_registration_with_method_returns_service_eager_node(self):
        class Service(object):
            def __init__(self, value, kvalue):
                self.value=value
                self.kvalue=kvalue
                self.mvalue=None
                self.mkwarg = None 

            def method1(self, marg, mkwarg):
                self.marg = marg
                self.mkwarg = mkwarg

        factory = ServiceEagerNodeFactory()
        reg = ClassRegistration(
            'class_registration_id',
            Service,
            lambda c: c('arg1', kvalue='keywordarg1'),
            [
                ('method1', lambda c: c('meth1arg1', mkwarg='meth1kwarg1')),
            ]
        )

        service_map = {
          'arg1': 'argument1',
          'keywordarg1':  'keyword argument one',
          'meth1arg1':  'method argument',
          'meth1kwarg1':  'method keyword argument'
        }

        service_eager_node = factory.from_registration(reg, service_map)
        service = service_eager_node.get_value()
        self.assertEqual(service.value, 'argument1')
        self.assertEqual(service.kvalue, 'keyword argument one')
        self.assertEqual(service.marg, 'method argument')
        self.assertEqual(service.mkwarg, 'method keyword argument')


class ParameterEagerNodeTestCase(TestCase):
    def test_constructor(self):
        node = ParameterEagerNode('foo', 'param')

    def test_get_value(self):
        node = ParameterEagerNode('foo', 'param')
        self.assertEqual('param', node.get_value())


class FunctionEagerNodeTestCase(TestCase):
    def test_constructor(self):
        node = FunctionEagerNode('foo', lambda: None)

    def test_get_value(self):
        func = lambda: None
        node = FunctionEagerNode('foo', func)
        self.assertEqual(func, node.get_value())


class ServiceEagerNodeTestCase(TestCase):
    def test_constructor(self):
        instance = FixtureService('Fix')
        node = ServiceEagerNode('foo', instance)

    def test_get_value(self):
        instance = FixtureService('Fix')
        node = ServiceEagerNode('foo', instance)
        self.assertEqual(instance, node.get_value())


class EagerDependencyInjectionCompilerTestCase(TestCase):
    def test_compile(self):
        graph = Graph()

        graph.register(
            ParameterRegistration('reg1', 'param')
        )
        graph.register(
            ClassRegistration(
                'reg2',
                FixtureService,
                lambda c: c('reg1')
            )
        )

        compiler = EagerDependencyInjectionCompiler()
        compiler.compile(graph)
        # Not raising the error is the test

    def test_slightly_complex_graph(self):
        graph = Graph()

        def function_reference(foo):
            return 1 + foo

        graph.register(
            FunctionRegistration(
                'meth2kwarg1',
                function_reference,
                lambda c: c(foo='p1')
            )
        )

        graph.register(
            ParameterRegistration('meth1arg1', 10)
        )

        graph.register(
            ParameterRegistration('p1', 100)
        )

        graph.register(
            ClassRegistration('reg1',
                FixtureService,
                lambda c: c('p1')
            )
        )
        graph.register(
            ClassRegistration(
                'reg2',
                FixtureService,
                lambda c: c('reg1'),
                [
                    ('method1', lambda c: c('meth1arg1')),
                    ('method2', lambda c: c('meth2kwarg1')),
                ]
            )
        )

        compiler = EagerDependencyInjectionCompiler()
        compiled = compiler.compile(graph)

        service = compiled.get_node_by_id('reg2').get_value()

        self.assertEqual(service.value.value, 100)
        self.assertEqual(service.method1_value, 10)
        self.assertEqual(service.method2_value(), 101)
        # Not raising the error is the test
