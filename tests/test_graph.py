from unittest import TestCase

from brap.graph import Graph, ServiceNode, GraphAnalyzer


class FixtureService(object):
    """
    Only used to provide a sample for tests
    """
    def __init__(self, value):
        self.value = value


class GraphTestCase(TestCase):
    def test_create_graph(self):
        graph = Graph()
        self.assertTrue(isinstance(graph, Graph))

    def test_create_service_node(self):
        serviceNode = ServiceNode(
            'ServiceNode',
            ['service','service1']
        )
        self.assertTrue(isinstance(serviceNode, ServiceNode))

    def test_create_service_node_returns_id(self):
        serviceNode = ServiceNode(
            'ServiceNode',
            ['service','service1']
        )
        self.assertEqual('ServiceNode', serviceNode.get_id())

    def test_nodes_added_to_graph_can_be_retrieved(self):
        graph = Graph()

        serviceNode1 = ServiceNode('ServiceNode1')
        serviceNode2 = ServiceNode('ServiceNode2')

        graph.add_node(serviceNode1)
        graph.add_node(serviceNode2)

        self.assertEqual('ServiceNode1', graph.get_node_by_id('ServiceNode1').get_id())
        self.assertEqual('ServiceNode2', graph.get_node_by_id('ServiceNode2').get_id())

    def test_duplicate_node_id_rejection(self):
        graph = Graph()

        serviceNode1 = ServiceNode('common_id')
        serviceNode2 = ServiceNode('common_id')

        with self.assertRaises(ValueError):  # TODO more specific exception
            graph.add_node(serviceNode1)
            graph.add_node(serviceNode2)

    def test_create_node_with_dependency(self):
        graph = Graph()

        serviceNode1 = ServiceNode('ServiceNode1')
        serviceNode2 = ServiceNode('ServiceNode2', ['ServiceNode1'])
        serviceNode3 = ServiceNode('ServiceNode3', ['ServiceNode2', 'ServiceNode1'])

        graph.add_node(serviceNode1)
        graph.add_node(serviceNode2)
        graph.add_node(serviceNode3)

        self.assertEqual([
            ('ServiceNode1', []),
            ('ServiceNode2', ['ServiceNode1']),
            ('ServiceNode3', ['ServiceNode2', 'ServiceNode1']),
        ], graph.get_dependency_lists())

    def test_create_node_with_unregistered_dependency(self):
        graph = Graph()

        serviceNode1 = ServiceNode('ServiceNode1', ['Unregistered'])

        graph.add_node(serviceNode1)

        self.assertEqual([
            ('Unregistered', []),
            ('ServiceNode1', ['Unregistered']),
        ], graph.get_dependency_lists())

    def test_create_node_with_unregistered_dependency_complex(self):
        graph = Graph()

        serviceNode1 = ServiceNode('ServiceNode1')
        serviceNode2 = ServiceNode('ServiceNode2', ['ServiceNode1'])
        serviceNode3 = ServiceNode('ServiceNode3', ['ServiceNode2', 'Unregistered'])

        graph.add_node(serviceNode1)
        graph.add_node(serviceNode2)
        graph.add_node(serviceNode3)

        self.assertEqual([
            ('ServiceNode1', []),
            ('ServiceNode2', ['ServiceNode1']),
            ('Unregistered', []),
            ('ServiceNode3', ['ServiceNode2', 'Unregistered'])
        ], graph.get_dependency_lists())


class GraphAnalyzerTestCase(TestCase):
    def test_topological_sort_basic(self):
        graph = Graph()

        serviceNode1 = ServiceNode('ServiceNode1')
        serviceNode2 = ServiceNode('ServiceNode2', ['ServiceNode1'])

        graph.add_node(serviceNode1)
        graph.add_node(serviceNode2)

        analysis = GraphAnalyzer(graph)

        self.assertEqual([], analysis.get_unregistered_nodes())
        self.assertEqual([], analysis.get_circular_dependencies())
        self.assertEqual(
            ['ServiceNode1', 'ServiceNode2'],
            [node.get_id() for node in analysis.get_sorted_nodes()]
        )

    def test_topological_sort_complex(self):
        graph = Graph()

        serviceNode1 = ServiceNode('ServiceNode1')
        serviceNode2 = ServiceNode('ServiceNode2', ['ServiceNode1'])
        serviceNode3 = ServiceNode('ServiceNode3', ['ServiceNode2', 'Unregistered'])
        serviceNode4 = ServiceNode('ServiceNode4', ['ServiceNode2', 'Unregistered'])

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
        self.assertEqual(
            [
                'ServiceNode1',
                'ServiceNode2',
                'Unregistered',
                'ServiceNode3',
                'ServiceNode4'
            ],
            [node.get_id() for node in analysis.get_sorted_nodes()]
        )

    def test_topological_sort_with_cycles(self):
        graph = Graph()

        serviceNode1 = ServiceNode('ServiceNode1', ['ServiceNode3'])
        serviceNode2 = ServiceNode('ServiceNode2', ['ServiceNode1'])
        serviceNode3 = ServiceNode('ServiceNode3', ['ServiceNode2'])

        graph.add_node(serviceNode1)
        graph.add_node(serviceNode2)
        graph.add_node(serviceNode3)

        analysis = GraphAnalyzer(graph)

        self.assertEqual([], analysis.get_unregistered_nodes())
        self.assertEqual(  # FIXME, order is irrelevant here.
            [
                'ServiceNode3',
                'ServiceNode1',
                'ServiceNode2',
            ],
            [node.get_id() for node in analysis.get_circular_dependencies()]
        )

#       self.assertEqual(s1, s1_retrieved_twice)

#       with self.assertRaises(Exception):
#           container.get('not_a_real_id')

#       self.assertTrue(isinstance(fixture_service))
