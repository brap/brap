from unittest import TestCase

from tests.fixtures import FixtureService

from brap.nodes import RegisteredNode
from brap.graph import Graph

from brap.compilers.eager_dependency_injection_compiler import (
    EagerDependencyInjectionCompiler,
    ServiceEagerNode,
    ParameterEagerNode,
    FunctionEagerNode
)

from brap.node_registrations import (
    ParameterRegistration,
    ClassRegistration,
)


class ParameterEagerNodeFactoryTestCase(TestCase):
    pass


class FunctionEagerNodeFactoryTestCase(TestCase):
    pass


class ServiceEagerNodeFactoryTestCase(TestCase):
    pass


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
            ClassRegistration('reg1', FixtureService)
        )
        graph.register(
            ClassRegistration(
                'reg2',
                FixtureService,
                lambda c: c()
            )
        )

        compiler = EagerDependencyInjectionCompiler()
        compiler.compile(graph)
        # Not raising the error is the test

    def test_(self):
        graph = Graph()

        graph.register(
            ClassRegistration('reg1', FixtureService)
        )
        graph.register(
            ClassRegistration(
                'reg2',
                FixtureService,
                lambda c: c()
            )
        )

        compiler = EagerDependencyInjectionCompiler()
        compiler.compile(graph)
        # Not raising the error is the test
