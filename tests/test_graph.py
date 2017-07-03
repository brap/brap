from unittest import TestCase

from brap.graph import Graph, ServiceNode


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
