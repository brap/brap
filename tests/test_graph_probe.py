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
            FixtureService
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
            FixtureService,
            lambda c: c('child')
        )
        container.set(
            'child',
            FixtureService
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
            FixtureService,
            lambda c: c('child-1', 'child-2')
        )
        container.set(
            'child-1',
            FixtureService,
        )
        container.set(
            'child-2',
            FixtureService,
        )
        #  TODO

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
            FixtureService,
            lambda c: c('child-1', 'child-2')
        )
        container.set(
            'child-1',
            FixtureService,
            lambda c: c('child-1-2')  # The graph is aware of an UnregisteredNode
        )
        container.set(
            'child-2',
            FixtureService,
            lambda c: c('child-2-2')
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
            FixtureService,
            lambda c: c('parent')
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
            FixtureService,
            lambda c: c('child')
        )
        container.set(
            'child',
            FixtureService,
            lambda c: c('parent')
        )
        #  TODO


# TODO also test on method injection
