from unittest import TestCase

from brap.container import Container, ProviderInterface


class FixtureService(object):
    """
    Only used to provide a sample for tests
    """
    def __init__(self, value):
        self.value = value


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

    def test_set_and_get_by_id_for_lambda(self):
        container = Container()
        container.set('fixture_service', lambda container: FixtureService(1))
        fixture_service = container.get('fixture_service')

        self.assertTrue(isinstance(fixture_service, FixtureService))

    def test_set_and_get_by_id_for_strings(self):
        container = Container()
        container.set('param', 'Some param')
        param = container.get('param')

        self.assertEqual('Some param', param)

    def test_two_containers_do_not_share_services(self):
        container = Container()
        container.set('ser1', lambda container: FixtureService(1))
        container.set('ser2', lambda container: FixtureService(2))

        s1 = container.get('ser1')
        s2 = container.get('ser2')
        self.assertEqual(1, s1.value)
        self.assertEqual(2, s2.value)

    def test_service_returns_same_object(self):
        container = Container()
        container.set('ser1', lambda container: FixtureService(1))

        s1 = container.get('ser1')
        s1_retrieved_twice = container.get('ser1')
        self.assertEqual(s1, s1_retrieved_twice)

    def test_container_is_provided_to_lambda(self):
        container = Container()
        container.set('param', 'Some param')

        container.set(
            'ser',
            lambda c: FixtureService(c.get('param'))
        )

        ser = container.get('ser')
        self.assertEqual('Some param', ser.value)

    def test_none_is_a_valid_parameter(self):
        container = Container()
        container.set('param', None)
        param = container.get('param')
        self.assertEqual(None, param)

    def test_set_by_factory_and_get_by_id(self):
        container = Container()

        container.factory(
            'factory',
            lambda container: FactoryFixture()
        )
        fac1 = container.get('factory')
        fac2 = container.get('factory')

        self.assertNotEqual(fac1, fac2)

    def test_register_provider(self):
        class FixtureProvider(ProviderInterface):
            def register(self, c):
                container.set(
                    'fixture_provided_service',
                    lambda container: FixtureService(c.get('param'))
                )

        container = Container()
        container.register(FixtureProvider())  # Intentionally defined before fixture_param.
        container.set('param', 'fixture_param')  # Intentionally defined after registering provider to ensure lazy loading.
        provided = container.get('fixture_provided_service')

        self.assertEqual('fixture_param', provided.value)
