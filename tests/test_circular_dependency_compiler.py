from unittest import TestCase

from tests.fixtures import FixtureService

from brap.nodes import RegisteredNode
from brap.graph import Graph

from brap.compilers.circular_dependency_compiler import (
    CircularDependencyCompiler,
    GraphSorter,
    NodeVisitor
)

from brap.node_registrations import (
    ParameterRegistration,
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
        # Not raising the error is the test

    def test_compile_circular_dep(self):
        graph = Graph()

        graph.register(
            ClassRegistration(
                'reg1',
                FixtureService,
                lambda c: c('reg2')
            )
        )
        graph.register(
            ClassRegistration(
                'reg2',
                FixtureService,
                lambda c: c('reg1')
            )
        )

        compiler = CircularDependencyCompiler()
        with self.assertRaises(Exception):
            compiler.compile(graph)


class GraphSorterTestCase(TestCase):
    def test_topological_sort_basic(self):
        graph = Graph()

        reg1 = ParameterRegistration('reg1', 'r1')
        reg2 = ClassRegistration('reg2', FixtureService, lambda c: c('reg1'))

        graph.register(reg1)
        graph.register(reg2)

        analysis = GraphSorter(graph)

        self.assertEqual([], analysis.get_circular_dependencies())
        self.assertEqual(
            set(['reg1', 'reg2']),
            set([node.get_id() for node in analysis.get_sorted_nodes()])
        )

    def test_topological_sort_complex_with_unregistered(self):
        graph = Graph()

        reg1 = ClassRegistration('reg1', FixtureService)
        reg2 = ClassRegistration('reg2', FixtureService, lambda c: c('reg1'))
        reg3 = ClassRegistration('reg3', FixtureService, lambda c: c('reg2', 'unregistered'))
        reg4 = ClassRegistration('reg4', FixtureService, lambda c: c('reg2', 'unregistered'))


        graph.register(reg1)
        graph.register(reg2)
        graph.register(reg3)
        graph.register(reg4)

        analysis = GraphSorter(graph)

        self.assertEqual([], analysis.get_circular_dependencies())

    def test_topological_sort_with_cycles(self):
        graph = Graph()

        reg1 = ClassRegistration('reg1', FixtureService, lambda c: c('reg2'))
        reg2 = ClassRegistration('reg2', FixtureService, lambda c: c('reg3'))
        reg3 = ClassRegistration('reg3', FixtureService, lambda c: c('reg1'))

        graph.register(reg1)
        graph.register(reg2)
        graph.register(reg3)

        analysis = GraphSorter(graph)

        self.assertEqual(
            set([
                'reg1',
                'reg2',
                'reg3'
            ]),
            set([node.get_id()
                    for node in analysis.get_circular_dependencies()])
        )
