from unittest import TestCase
from unittest.mock import MagicMock
import uuid  # Used to ensure multiple results are different

from tests.fixtures import FixtureService, FactoryFixture

from brap.container import Container


class ContainerTestCase(TestCase):
    def test_get_invalid_id(self):
        container = Container()
        with self.assertRaises(Exception):
            container.get('not_a_real_id')

    def test_set_and_get_by_id_for_class(self):
        spy_graph = MagicMock()
        container = Container(spy_graph)
        container.set('fixture_service_param', 1)
        container.set(
            'fixture_service',
            FixtureService,
            lambda c: c('fixture_service_param')
        )
        container.get('fixture_service')
        spy_graph.get_node_by_id.assert_called_with('fixture_service')

    def test_set_and_get_by_id_with_kwarg_for_class(self):
        spy_graph = MagicMock()
        container = Container(spy_graph)
        container.set('fixture_service_param', 1)
        container.set(
            'fixture_service',
            FixtureService,
            lambda c: c(value='fixture_service_param')
        )
        container.get('fixture_service')

        spy_graph.get_node_by_id.assert_called_with('fixture_service')

    def test_set_and_get_by_id_for_strings(self):
        spy_graph = MagicMock()
        container = Container(spy_graph)
        container.set('param', 'Some param')
        container.get('param')

        node = spy_graph.get_node_by_id.assert_called_with('param')

    def test_merge(self):
        spy_graph1 = MagicMock()
        container1 = Container(spy_graph1)

        spy_graph2 = MagicMock()
        container2 = Container(spy_graph2)

        container1.merge(container2)

        node = spy_graph1.merge.assert_called_with(spy_graph2)
