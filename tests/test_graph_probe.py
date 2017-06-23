from unittest import TestCase

from brap.container import Container, ProviderInterface


class FixtureService(object):
    """
    Only used to provide a sample for tests
    """
    def __init__(self, value):
        self.value = value


class ContainerTestCase(TestCase):
    def test_single_node(self):
        """
        Nodes:
            parent
        """
        container = Container()
        container.set(
            'parent',
            lambda c: FixtureService('parent')
        )
        #  TODO

    def test_node_with_one_child(self):
        """
        Nodes:
            parent
            └── child
        """
        container = Container()
        container.set(
            'parent',
            lambda c: FixtureService(c.get('child'))
        )
        container.set(
            'child',
            lambda c: FixtureService('child')
        )
        #  TODO

    def test_node_with_two_children(self):
        """
        Nodes:
            parent
            ├── child-1
            └── child-2
        """
        container = Container()
        container.set(
            'parent',
            lambda c: FixtureService(c.get('child-1'), c.get('child-2'))
        )
        container.set(
            'child-1',
            lambda c: FixtureService('child-1')
        )
        container.set(
            'child-2',
            lambda c: FixtureService('child-2')
        )
        #  TODO

        container.set('param', 'Some param')
        param = container.get('param')

        self.assertEqual('Some param', param)

    def test_node_with_two_children_each_with_two_children(self):
        """
        Nodes:
            parent
            ├── child-1
            │   ├── child-1-1
            │   └── child-1-2
            └── child-2
                ├── child-2-1
                └── child-2-2
        """
        container = Container()
        container.set(
            'parent',
            lambda c: FixtureService(c.get('child-1'), c.get('child-2'))
        )
        container.set(
            'child-1-1',
            lambda c: FixtureService(c.get('child-1-2')
        )
        container.set(
            'child-2-1',
            lambda c: FixtureService(c.get('child-2-2')
        )
        container.set(
            'child-1-2',
            lambda c: FixtureService('child-1-2')
        )
        container.set(
            'child-2-2',
            lambda c: FixtureService('child-2-2')
        )
        #  TODO

    def test_node_which_depends_on_self(self):
        """
        Nodes:
            parent
            └── parent
                └── parent
                    └── parent
                        ...
        """
        container = Container()
        container.set(
            'parent',
            lambda c: FixtureService(c.get('parent'))
        )
        #  TODO

    def test_with_child_which_depends_on_parent(self):
        """
        Nodes:
            parent
            └── child
                └── parent
                    └── child
                        └── parent
                           ....
        """
        container = Container()
        container.set(
            'parent',
            lambda c: FixtureService(c.get('child'))
        )
        container.set(
            'child',
            lambda c: FixtureService(c.get('parent'))
        )
        #  TODO

