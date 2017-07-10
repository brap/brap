from unittest import TestCase

from tests.fixtures import FixtureService

from brap.graph import Graph
from brap.compilers.edge_node_compiler import EdgeNodeCompiler
from brap.node_registrations import ClassRegistration


class EdgeNodeCompilerTestCase(TestCase):
    def test_compile(self):
        graph = Graph()

        graph.register(
            ClassRegistration('reg1', FixtureService)
        )
        graph.register(
            ClassRegistration(
                'reg2',
                FixtureService,
                lambda c: c('unregistered')
            )
        )

        compiler = EdgeNodeCompiler()
        compiler.compile(graph)
        graph.get_node_by_id('unregistered')
