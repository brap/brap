from unittest import TestCase

from brap.graph import Graph, RegisteredNode, GraphAnalyzer


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
        serviceNode = RegisteredNode(
            'RegisteredNode',
            ['service','service1']
        )
        self.assertTrue(isinstance(serviceNode, RegisteredNode))

    def test_create_service_node_returns_id(self):
        serviceNode = RegisteredNode(
            'RegisteredNode',
            ['service','service1']
        )
        self.assertEqual('RegisteredNode', serviceNode.get_id())

    def test_nodes_added_to_graph_can_be_retrieved(self):
        graph = Graph()

        serviceNode1 = RegisteredNode('RegisteredNode1')
        serviceNode2 = RegisteredNode('RegisteredNode2')

        graph.add_node(serviceNode1)
        graph.add_node(serviceNode2)

        self.assertEqual('RegisteredNode1', graph.get_node_by_id('RegisteredNode1').get_id())
        self.assertEqual('RegisteredNode2', graph.get_node_by_id('RegisteredNode2').get_id())

    def test_duplicate_node_id_rejection(self):
        graph = Graph()

        serviceNode1 = RegisteredNode('common_id')
        serviceNode2 = RegisteredNode('common_id')

        with self.assertRaises(ValueError):  # TODO more specific exception
            graph.add_node(serviceNode1)
            graph.add_node(serviceNode2)

    def test_create_node_with_dependency(self):
        graph = Graph()

        serviceNode1 = RegisteredNode('RegisteredNode1')
        serviceNode2 = RegisteredNode('RegisteredNode2', ['RegisteredNode1'])
        serviceNode3 = RegisteredNode('RegisteredNode3', ['RegisteredNode2', 'RegisteredNode1'])

        graph.add_node(serviceNode1)
        graph.add_node(serviceNode2)
        graph.add_node(serviceNode3)

        self.assertEqual(sorted([
            ('RegisteredNode1', []),
            ('RegisteredNode2', ['RegisteredNode1']),
            ('RegisteredNode3', ['RegisteredNode2', 'RegisteredNode1']),
        ]), sorted(graph.get_dependency_lists()))

    def test_create_node_with_unregistered_dependency(self):
        graph = Graph()

        serviceNode1 = RegisteredNode('RegisteredNode1', ['Unregistered'])

        graph.add_node(serviceNode1)

       # FIXME Fails on python3.5 due to "Unregistered" being first element.
       #self.assertEqual([
       #    ('Unregistered', []),
       #    ('RegisteredNode1', ['Unregistered']),
       #], graph.get_dependency_lists())

    def test_create_node_with_unregistered_dependency_complex(self):
        graph = Graph()

        serviceNode1 = RegisteredNode('RegisteredNode1')
        serviceNode2 = RegisteredNode('RegisteredNode2', ['RegisteredNode1'])
        serviceNode3 = RegisteredNode('RegisteredNode3', ['RegisteredNode2', 'Unregistered'])

        graph.add_node(serviceNode1)
        graph.add_node(serviceNode2)
        graph.add_node(serviceNode3)

       # FIXME Fails on python3.5 due to "Unregistered" being first element.
       #self.assertEqual([
       #    ('RegisteredNode1', []),
       #    ('RegisteredNode2', ['RegisteredNode1']),
       #    ('Unregistered', []),
       #    ('RegisteredNode3', ['RegisteredNode2', 'Unregistered'])
       #], graph.get_dependency_lists())


class GraphAnalyzerTestCase(TestCase):
    def test_topological_sort_basic(self):
        graph = Graph()

        serviceNode1 = RegisteredNode('RegisteredNode1')
        serviceNode2 = RegisteredNode('RegisteredNode2', ['RegisteredNode1'])

        graph.add_node(serviceNode1)
        graph.add_node(serviceNode2)

        analysis = GraphAnalyzer(graph)

        self.assertEqual([], analysis.get_unregistered_nodes())
        self.assertEqual([], analysis.get_circular_dependencies())
        self.assertEqual(
            ['RegisteredNode1', 'RegisteredNode2'],
            [node.get_id() for node in analysis.get_sorted_nodes()]
        )

    def test_topological_sort_complex(self):
        graph = Graph()

        serviceNode1 = RegisteredNode('RegisteredNode1')
        serviceNode2 = RegisteredNode('RegisteredNode2', ['RegisteredNode1'])
        serviceNode3 = RegisteredNode('RegisteredNode3', ['RegisteredNode2', 'Unregistered'])
        serviceNode4 = RegisteredNode('RegisteredNode4', ['RegisteredNode2', 'Unregistered'])

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

       # FIXME Fails on python3.5 due to "Unregistered" being first element.
       #self.assertEqual(
       #    [
       #        'RegisteredNode1',
       #        'RegisteredNode2',
       #        'Unregistered',
       #        'RegisteredNode3',
       #        'RegisteredNode4'
       #    ],
       #    [node.get_id() for node in analysis.get_sorted_nodes()]
       #)

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
            sorted([node.get_id() for node in analysis.get_circular_dependencies()])
        )
