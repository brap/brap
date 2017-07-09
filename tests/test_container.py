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


# TODO test these at integration level, good things to check, but not valuable
# as unit tests
#   def test_two_containers_do_not_share_services(self):
#       spy_graph1 = MagicMock()
#       container1 = Container(spy_graph1)

#       spy_graph2 = MagicMock()
#       container2 = Container(spy_graph2)

#       container1.set('fixture_service_param', 'container1')
#       container2.set('fixture_service_param', 'container2')

#       # Intentionally giving services same id
#       container1.set('ser1', FixtureService,
#           lambda c: c('fixture_service_param'))
#       container2.set('ser1', FixtureService,
#           lambda c: c('fixture_service_param'))

#       s1 = container1.get('ser1')
#       s2 = container2.get('ser1')
#       self.assertEqual('container1', s1.value)
#       self.assertEqual('container2', s2.value)

#   def test_service_returns_same_object(self):
#       container = Container()
#       container.set('fixture_service_param', 'container1')
#       container.set('ser1', FixtureService,
#           lambda c: c('fixture_service_param'))

#       s1 = container.get('ser1')
#       s1_retrieved_twice = container.get('ser1')
#       self.assertEqual(s1, s1_retrieved_twice)

#   def test_none_is_a_valid_parameter(self):
#       container = Container()
#       container.set('param', None)
#       param = container.get('param')
#       self.assertEqual(None, param)

#   def test_set_by_factory_and_get_by_id(self):
#       container = Container()

#       container.factory('factory', FactoryFixture)
#       fac1 = container.get('factory')
#       fac2 = container.get('factory')

#       self.assertNotEqual(fac1, fac2)

#   def test_set_and_get_by_id_for_class_with_method_calls(self):
#       container = Container()

#       # I mix short and long form names to test against the key/value being
#       # confused internally
#       container.set('const_param', 'constructor_param')
#       container.set('meth_param', 'method_param')
#       container.set('fixture_service',
#                     FixtureService,
#                     lambda c: c('const_param'),
#                     [
#                         ('set_other_value', lambda c: c('meth_param'))
#                     ]
#                     )
#       fixture_service = container.get('fixture_service')
#       self.assertEqual(fixture_service.value, 'constructor_param')
#       self.assertEqual(fixture_service.other_value, 'method_param')

#   def test_set_and_get_by_id_for_class_with_method_calls_with_kwargs(self):
#       container = Container()

#       # I mix short and long form names to test against the key/value being
#       # confused internally
#       container.set('const_param', 'constructor_param')
#       container.set('meth_param', 'method_param')
#       container.set('fixture_service',
#               FixtureService,
#               lambda c: c('const_param'),
#               [
#                   ('set_other_value', lambda c: c(other_value='meth_param'))
#               ]
#           )
#       fixture_service = container.get('fixture_service')
#       self.assertEqual(fixture_service.value, 'constructor_param')
#       self.assertEqual(fixture_service.other_value, 'method_param')
