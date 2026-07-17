#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Contracts for preserving additive Request hook registration."""

import unittest

from requests.hooks import dispatch_hook
from requests.models import Request


class RequestHookRegistrationContractTest(unittest.TestCase):

    def test_HOOKS_007_constructor_hooks_and_subsequent_same_name_hook_remain_registered(self):
        """GUID: HOOKS-007 - later registration preserves constructor hooks."""
        def constructor_hook_a(value):
            return value

        def constructor_hook_b(value):
            return value

        def subsequent_hook(value):
            return value

        request = Request(hooks={
            'response': [constructor_hook_a, constructor_hook_b],
        })
        request.register_hook('response', subsequent_hook)

        self.assertEqual(request.hooks['response'], [
            constructor_hook_a,
            constructor_hook_b,
            subsequent_hook,
        ])

    def test_HOOKS_009_repeated_direct_registration_preserves_each_hook_entry(self):
        """GUID: HOOKS-009 - repeated direct calls remain additive."""
        def hook_a(value):
            return value

        def hook_b(value):
            return value

        def hook_c(value):
            return value

        request = Request()
        request.register_hook('response', hook_a)
        request.register_hook('response', hook_b)
        request.register_hook('response', hook_c)

        self.assertEqual(request.hooks['response'], [hook_a, hook_b, hook_c])

    def test_HOOKS_007_HOOKS_009_mixed_repeated_registration_discards_no_prior_hook(self):
        """GUID: HOOKS-007, HOOKS-009 - no later call replaces a prior hook."""
        calls = []

        def constructor_hook(value):
            calls.append('constructor')
            return value

        def direct_hook_a(value):
            calls.append('direct-a')
            return value

        def direct_hook_b(value):
            calls.append('direct-b')
            return value

        request = Request(hooks={'response': constructor_hook})
        request.register_hook('response', direct_hook_a)
        request.register_hook('response', direct_hook_b)

        hook_data = object()
        result = dispatch_hook('response', request.hooks, hook_data)

        self.assertEqual(calls, ['constructor', 'direct-a', 'direct-b'])
        self.assertIs(result, hook_data)
