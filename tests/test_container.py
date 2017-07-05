from unittest import TestCase
import uuid  # Used to ensure multiple results are different

from brap.container import Container, ProviderInterface


class FixtureService(object):
    """
    Only used to provide a sample for tests
    """

    def __init__(self, value):
        self.value = value
        self.other_value = None

    def set_other_value(self, other_value):
        self.other_value = other_value


class FactoryFixture(object):
    """
    Only used to provide a sample for tests
    """

    def __init__(self):
        pass


class ContainerTestCase(TestCase):
    def test_get_invalid_id(self):
        container = Container()
        with self.assertRaises(Exception):
            container.get('not_a_real_id')

    def test_set_and_get_by_id_for_class(self):
        container = Container()
        container.set('fixture_service_param', 1)
        container.set('fixture_service', FixtureService,
                      ['fixture_service_param'])
        fixture_service = container.get('fixture_service')

        self.assertTrue(isinstance(fixture_service, FixtureService))

    def test_set_and_get_by_id_for_strings(self):
        container = Container()
        container.set('param', 'Some param')
        param = container.get('param')

        self.assertEqual('Some param', param)

    def test_set_and_get_by_id_for_class(self):
        container = Container()

        def test_fn():
            return uuid.uuid4()

        container.set('fn', test_fn)
        call1 = container.get('fn')
        call2 = container.get('fn')

        self.assertNotEqual(call1, call2)

    def test_two_containers_do_not_share_services(self):
        container1 = Container()
        container2 = Container()

        container1.set('fixture_service_param', 'container1')
        container2.set('fixture_service_param', 'container2')

        # Intentionally giving services same id
        container1.set('ser1', FixtureService, ['fixture_service_param'])
        container2.set('ser1', FixtureService, ['fixture_service_param'])

        s1 = container1.get('ser1')
        s2 = container2.get('ser1')
        self.assertEqual('container1', s1.value)
        self.assertEqual('container2', s2.value)

    def test_service_returns_same_object(self):
        container = Container()
        container.set('fixture_service_param', 'container1')
        container.set('ser1', FixtureService, ['fixture_service_param'])

        s1 = container.get('ser1')
        s1_retrieved_twice = container.get('ser1')
        self.assertEqual(s1, s1_retrieved_twice)

    def test_none_is_a_valid_parameter(self):
        container = Container()
        container.set('param', None)
        param = container.get('param')
        self.assertEqual(None, param)

    def test_set_by_factory_and_get_by_id(self):
        container = Container()

        container.factory('factory', FactoryFixture)
        fac1 = container.get('factory')
        fac2 = container.get('factory')

        self.assertNotEqual(fac1, fac2)

    def test_set_and_get_by_id_for_class_with_method_calls(self):
        container = Container()

        # I mix short and long form names to test against the key/value being confused internally
        container.set('const_param', 'constructor_param')
        container.set('meth_param', 'method_param')
        container.set('fixture_service',
                      FixtureService,
                      ['const_param'],
                      [
                          ('set_other_value', ['meth_param'])
                      ]
                      )
        fixture_service = container.get('fixture_service')
        self.assertEqual(fixture_service.value, 'constructor_param')
        self.assertEqual(fixture_service.other_value, 'method_param')

    def test_register_provider(self):
        class FixtureProvider(ProviderInterface):
            def register(self, container):
                container.set(
                    'fixture_provided_service',
                    FixtureService,
                    ['param']
                )

        container = Container()
        # Intentionally defined before fixture_param.
        container.registerProvider(FixtureProvider())
        # Intentionally defined after registering provider to ensure lazy loading.
        container.set('param', 'fixture_param')
        provided = container.get('fixture_provided_service')

        self.assertEqual('fixture_param', provided.value)
