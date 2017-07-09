from unittest import TestCase

from tests.fixtures import FixtureService

from brap.node_registrations import (
    ParameterRegistration,
    FunctionRegistration,
    ClassRegistration,
    extract_edges_from_callable
)

function_reference = lambda: None

class Extract_Edges_From_CallableTestCase(TestCase):
    def test_extract_edges_from_callable(self):
        callable = lambda c: c('a', 'b', kwarg_c='c', kwarg_d='d')
        edges = extract_edges_from_callable(callable)
        self.assertEqual(['a', 'b', 'c', 'd'], edges)

    def test_extract_args_from_callable(self):
        callable = lambda c: c('a', 'b')
        edges = extract_edges_from_callable(callable)
        self.assertEqual(['a', 'b'], edges)

    def test_extract_kwargs_from_callable(self):
        callable = lambda c: c(kwarg_c='c', kwarg_d='d')
        edges = extract_edges_from_callable(callable)
        self.assertEqual(['c', 'd'], edges)

    def test_extract_without_strings_is_exception(self):
        callable = lambda c: c('a', 'b', kwarg_c='c', kwarg_d='d')
        edges = extract_edges_from_callable(callable)
        self.assertEqual(['a', 'b', 'c', 'd'], edges)

    def test_extract_without_strings_is_exception(self):
        callable = lambda c: c(1)
        with self.assertRaises(ValueError):  # TODO more specific exception
            edges = extract_edges_from_callable(callable)

    def test_extract_without_strings_no_params(self):
        callable = lambda c: c()
        edges = extract_edges_from_callable(callable)
        self.assertEqual([], edges)


class ParameterRegistrationTestCase(TestCase):
    def test_create_registration(self):
        reg = ParameterRegistration(
            'param_registration',
            'param_registration_value'
        )
        self.assertTrue(isinstance(reg, ParameterRegistration))

    def test_create_registration_id(self):
        reg = ParameterRegistration(
            'param_registration',
            'param_registration_value'
        )
        self.assertEqual('param_registration', reg.get_id())

    def test_create_registration_edges(self):
        reg = ParameterRegistration(
            'param_registration',
            'param_registration_value'
        )
        self.assertEqual([], reg.get_edges())


class FunctionRegistrationTestCase(TestCase):

    def test_create_registration_no_call(self):
        reg = FunctionRegistration(
            'function_registration',
            function_reference,

        )
        self.assertTrue(isinstance(reg, FunctionRegistration))

    def test_create_registration_no_call_edges(self):
        reg = FunctionRegistration(
            'function_registration',
            function_reference,
        )
        self.assertEqual([], reg.get_edges())

    def test_create_registration_call_edges(self):
        reg = FunctionRegistration(
            'function_registration',
            function_reference,
            lambda c: c('arg1', kwarg1='keywordarg1')
        )
        self.assertEqual(['arg1', 'keywordarg1'], reg.get_edges())


class ClassRegistrationTestCase(TestCase):
    def test_create_registration_no_calls(self):
        reg = ClassRegistration(
            'class_registration',
            FixtureService
        )
        self.assertTrue(isinstance(reg, ClassRegistration))

    def test_create_registration_no_calls_edges(self):
        reg = ClassRegistration(
            'class_registration',
            FixtureService
        )
        self.assertEqual([], reg.get_edges())

    def test_create_registration_calls_edges(self):
        reg = ClassRegistration(
            'class_registration',
            FixtureService,
            lambda c: c('arg1', kwarg1='keywordarg1')
        )
        self.assertEqual(['arg1', 'keywordarg1'], reg.get_edges())

    def test_create_registration_calls_and_methods_edges(self):
        reg = ClassRegistration(
            'class_registration',
            FixtureService,
            lambda c: c('arg1', kwarg1='keywordarg1'),
            [
                ('method1', lambda c: c('method1arg1', kwarg1='method1keywordarg1')),
                ('method2', lambda c: c('method2arg1', kwarg1='method2keywordarg1'))
            ]
        )
        self.assertEqual([
            'arg1',
            'keywordarg1',
            'method1arg1',
            'method1keywordarg1',
            'method2arg1',
            'method2keywordarg1'
        ], reg.get_edges())
