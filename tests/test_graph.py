from unittest import TestCase

from tests.fixtures import FixtureService

from brap.graph import Graph
from brap.nodes import RegisteredNode
from brap.node_registrations import (
    ParameterRegistration,
    FunctionRegistration,
    ClassRegistration,
)


class GraphTestCase(TestCase):
    def test_create_graph(self):
        graph = Graph()
        self.assertTrue(isinstance(graph, Graph))

    def test_nodes_added_to_graph_can_be_retrieved(self):
        graph = Graph()

        reg1 = ParameterRegistration('reg1', 'v1')
        reg2 = ParameterRegistration('reg2', 'v2')

        graph.register(reg1)
        graph.register(reg2)

        self.assertEqual('reg1', graph.get_node_by_id('reg1').get_id())
        self.assertEqual('reg2', graph.get_node_by_id('reg2').get_id())

    def test_duplicate_node_id_rejection(self):
        graph = Graph()

        reg1 = ParameterRegistration('reg1', 'v1')
        reg2 = ParameterRegistration('reg1', 'v2')  # Intentionally same ID

        with self.assertRaises(ValueError):
            graph.register(reg1)
            graph.register(reg2)

    def test_create_node_with_dependency(self):
        graph = Graph()

        reg1 = ParameterRegistration('reg1', 'v1')
        reg2 = ParameterRegistration('reg2', 'v2')

        reg1 = ParameterRegistration('reg1', 'p1')
        reg2 = ClassRegistration('reg2', FixtureService, lambda c: c('reg1'))
        reg3 = ClassRegistration(
            'reg3',
            FixtureService,
            lambda c: c('reg1', 'reg2')
        )

        graph.register(reg1)
        graph.register(reg2)
        graph.register(reg3)

        self.assertEqual(['reg1', 'reg2', 'reg3'], list(graph.get_nodes()))

    def test_graph_merge_pre_existing(self):
        graph1 = Graph()
        graph2 = Graph()

        g1r = ParameterRegistration('r0', 'g1r')
        g2r = ParameterRegistration('r0', 'g2r')

        graph1.register(g1r)
        graph2.register(g2r)
        graph1.merge(graph2)

        self.assertEqual(['r0'], list(graph1.get_nodes()))

        # this is kind of hacky
        self.assertEqual(
            'g1r',
            graph1.get_node_by_id('r0')._registration._value
        )

    def test_graph_merge_new_nodes(self):
        graph1 = Graph()
        graph2 = Graph()

        g1r = ParameterRegistration('r0', 'g1r')
        g2r = ParameterRegistration('r1', 'g2r')

        graph1.register(g1r)
        graph2.register(g2r)
        graph1.merge(graph2)

        self.assertEqual(['r0', 'r1'], list(graph1.get_nodes()))
