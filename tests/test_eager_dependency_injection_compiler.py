from unittest import TestCase

from tests.fixtures import FixtureService

from brap.nodes import RegisteredNode
from brap.graph import Graph

from brap.compilers.eager_dependency_injection_compiler import (
    EagerDependencyInjectionCompiler
)

from brap.node_registrations import (
    ParameterRegistration,
    ClassRegistration,
)


class TestCase(TestCase):
    def test_(self):
        pass


class TestCase(TestCase):
    def test_(self):
        pass


class TestCase(TestCase):
    def test_(self):
        pass


class EagerDependencyInjectionCompilerTestCase(TestCase):
    def test_compile(self):
        graph = Graph()

        graph.register(
            ClassRegistration('reg1', FixtureService)
        )
        graph.register(
            ClassRegistration(
                'reg2',
                FixtureService,
                lambda c: c()
            )
        )

        compiler = EagerDependencyInjectionCompiler()
        compiler.compile(graph)
        # Not raising the error is the test

