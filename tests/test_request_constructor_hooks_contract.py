#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Behavioral contracts for constructor-supplied Request hooks."""

import unittest

from requests.hooks import dispatch_hook
from requests.models import Request


class RequestConstructorHooksContractTest(unittest.TestCase):

    def test_HOOKS_001_constructor_list_registers_each_callable_not_list(self):
        """GUID: HOOKS-001 - list values become separate hook entries."""
        def hook_a(value):
            return value

        def hook_b(value):
            return value

        configured_hooks = [hook_a, hook_b]
        request = Request(hooks={'response': configured_hooks})

        self.assertEqual(request.hooks['response'], [hook_a, hook_b])
        self.assertFalse(any(hook is configured_hooks
                             for hook in request.hooks['response']))

    def test_HOOKS_003_constructor_callable_registers_under_specified_hook(self):
        """GUID: HOOKS-003 - a single callable remains supported."""
        def hook_a(value):
            return value

        request = Request(hooks={'response': hook_a})

        self.assertEqual(request.hooks['response'], [hook_a])

    def test_HOOKS_005_constructor_list_preserves_callable_execution_order(self):
        """GUID: HOOKS-005 - list order survives registration."""
        calls = []

        def hook_a(value):
            calls.append('a')
            return value

        def hook_b(value):
            calls.append('b')
            return value

        request = Request(hooks={'response': [hook_a, hook_b]})
        dispatch_hook('response', request.hooks, object())

        self.assertEqual(calls, ['a', 'b'])

    def test_HOOKS_006_constructor_hooks_remain_exclusive_to_specified_names(self):
        """GUID: HOOKS-006 - callables do not cross hook-name boundaries."""
        def pre_send_hook(value):
            return value

        def response_hook(value):
            return value

        request = Request(hooks={
            'pre_send': [pre_send_hook],
            'response': [response_hook],
        })

        self.assertEqual(request.hooks['pre_send'], [pre_send_hook])
        self.assertEqual(request.hooks['response'], [response_hook])
        self.assertFalse(response_hook in request.hooks['pre_send'])
        self.assertFalse(pre_send_hook in request.hooks['response'])

    def test_HOOKS_008_constructor_list_element_uses_individual_validation(self):
        """GUID: HOOKS-008 - each element follows registration validation."""
        registrations = []

        class RecordingRequest(Request):

            def register_hook(self, event, hook):
                registrations.append((event, hook))
                Request.register_hook(self, event, hook)

        def hook_a(value):
            return value

        def hook_b(value):
            return value

        RecordingRequest(hooks={'response': [hook_a, hook_b]})

        self.assertEqual(registrations,
                         [('response', hook_a), ('response', hook_b)])
        self.assertRaises(KeyError, Request,
                          hooks={'unsupported': hook_a})
        self.assertRaises(KeyError, Request,
                          hooks={'unsupported': [hook_a]})
