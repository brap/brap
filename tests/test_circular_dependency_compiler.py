from unittest import TestCase

from tests.fixtures import FixtureService

from brap.nodes import RegisteredNode
from brap.graph import Graph

from brap.compilers.circular_dependency_compiler import (
    CircularDependencyCompiler,
    NodeVisitor
)

from brap.node_registrations import (
    ParameterRegistration,
    FunctionRegistration,
    ClassRegistration,
)


class NodeVisitorTestCase(TestCase):
    def test_instance_created_as_expected(self):
        reg = ParameterRegistration(
            'node_id',
            'param_registration_value'
        )
        node = RegisteredNode(reg)
        nv = NodeVisitor(node)

        self.assertTrue(isinstance(nv, NodeVisitor))

    def test_increment_and_decrement(self):
        reg = ParameterRegistration(
            'node_id',
            'param_registration_value'
        )
        node = RegisteredNode(reg)
        nv = NodeVisitor(node)

        self.assertEqual(0, nv.get_weight())
        nv.increment()
        self.assertEqual(1, nv.get_weight())
        nv.decrement()
        self.assertEqual(0, nv.get_weight())

    def test_get_id(self):
        reg = ParameterRegistration(
            'node_id',
            'param_registration_value'
        )
        node = RegisteredNode(reg)
        nv = NodeVisitor(node)

        self.assertEqual('node_id', nv.get_id())


class CircularDependencyCompilerTestCase(TestCase):
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

        compiler = CircularDependencyCompiler()
        compiler.compile(graph)
        #self.assertEqual(
        #    'unregistered',
        #    graph.get_node_by_id('unregistered').get_id()
        #)
