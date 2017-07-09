from unittest import TestCase

from tests.fixtures import FixtureService

from brap.nodes import RegisteredNode
from brap.node_registrations import ParameterRegistration

class NodesTestCase(TestCase):
    def test_create_service_node_with_registration(self):
        reg = ParameterRegistration(
            'param_registration',
            'param_registration_value'
        )
        node = RegisteredNode(reg)
        self.assertTrue(isinstance(node, RegisteredNode))

    def test_create_service_node_returns_id(self):
        reg = ParameterRegistration(
            'param_registration',
            'param_registration_value'
        )
        node = RegisteredNode(reg)
        self.assertEqual('param_registration', node.get_id())

    def test_create_service_node_returns_edges(self):
        reg = ParameterRegistration(
            'param_registration',
            'param_registration_value'
        )
        node = RegisteredNode(reg)
        self.assertEqual([], node.get_edges())

    def test_create_service_node_tags(self):
        reg = ParameterRegistration(
            'param_registration',
            'param_registration_value'
        )
        node = RegisteredNode(reg)
        node.set_tags(['a', 'b'])
        self.assertEqual(['a', 'b'], node.get_tags())
