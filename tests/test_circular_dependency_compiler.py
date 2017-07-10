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

        self.assertEqual(
            'unregistered',
            graph.get_node_by_id('unregistered').get_id()
        )

# TODO
class GraphSorterTestCase(TestCase):
    def test_topological_sort_basic(self):
        graph = Graph()

        reg1 = ParameterRegistration('reg1', 'r1')
        reg2 = ClassRegistration('reg2', FixtureService, lambda c: c('reg1'))

        serviceNode1 = RegisteredNode('RegisteredNode1')
        serviceNode2 = RegisteredNode('RegisteredNode2', ['RegisteredNode1'])

        graph.register(reg1)
        graph.register(reg2)

        analysis = GraphSorter(graph)

        self.assertEqual([], analysis.get_circular_dependencies())
        self.assertEqual(
            set(['RegisteredNode1', 'RegisteredNode2']),
            set([node.get_id() for node in analysis.get_sorted_nodes()])
        )

    def test_topological_sort_complex(self):
        graph = Graph()

        serviceNode1 = RegisteredNode('RegisteredNode1')
        serviceNode2 = RegisteredNode('RegisteredNode2', ['RegisteredNode1'])
        serviceNode3 = RegisteredNode(
            'RegisteredNode3', ['RegisteredNode2', 'Unregistered'])
        serviceNode4 = RegisteredNode(
            'RegisteredNode4', ['RegisteredNode2', 'Unregistered'])

        graph.add_node(serviceNode1)
        graph.add_node(serviceNode2)
        graph.add_node(serviceNode3)
        graph.add_node(serviceNode4)

        analysis = GraphAnalyzer(graph)

        self.assertEqual(
            ['Unregistered'],
            [node.get_id() for node in analysis.get_unregistered_nodes()]
        )
        self.assertEqual([], analysis.get_circular_dependencies())

    def test_topological_sort_with_cycles(self):
        graph = Graph()

        serviceNode1 = RegisteredNode('RegisteredNode1', ['RegisteredNode3'])
        serviceNode2 = RegisteredNode('RegisteredNode2', ['RegisteredNode1'])
        serviceNode3 = RegisteredNode('RegisteredNode3', ['RegisteredNode2'])

        graph.add_node(serviceNode1)
        graph.add_node(serviceNode2)
        graph.add_node(serviceNode3)

        analysis = GraphAnalyzer(graph)

        self.assertEqual([], analysis.get_unregistered_nodes())
        self.assertEqual(
            sorted([
                'RegisteredNode3',
                'RegisteredNode1',
                'RegisteredNode2',
            ]),
            sorted([node.get_id()
                    for node in analysis.get_circular_dependencies()])
        )
