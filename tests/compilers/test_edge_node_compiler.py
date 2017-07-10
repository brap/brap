from unittest import TestCase

from brap.nodes import RegisteredNode

from brap.compilers.edge_node_compiler import (
    EdgeNodeCompiler,
    NodeVisitor
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
