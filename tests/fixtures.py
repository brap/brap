from unittest import TestCase

from brap.graph import Graph

from brap.node_registrations import (
    ClassRegistration,
    FunctionRegistration,
    ParameterRegistration
)

class FixtureService(object):
    """
    Only used to provide a sample for tests
    """

    def __init__(self, value):
        self.value = value

    def method1(self, value):
        self.method1_value = value

    def method2(self, value):
        self.method2_value = value
