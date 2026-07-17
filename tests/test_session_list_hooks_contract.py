#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Behavioral contracts for consuming list-valued hooks through sessions."""

import unittest

from requests.hooks import dispatch_hook
from requests.models import Request
from requests.sessions import Session


class SessionListHooksContractTest(unittest.TestCase):

    def test_HOOKS_002_consuming_list_hook_invokes_each_function_not_list(self):
        """GUID: HOOKS-002 - consume each registered function separately."""
        calls = []

        def hook_a(value):
            calls.append(('a', value))
            return 'from-a'

        def hook_b(value):
            calls.append(('b', value))
            return 'from-b'

        configured_hooks = [hook_a, hook_b]
        result = dispatch_hook('response',
                               {'response': configured_hooks},
                               'original')

        self.assertEqual(calls, [('a', 'original'), ('b', 'from-a')])
        self.assertEqual(result, 'from-b')

    def test_HOOKS_004_session_create_send_preserves_all_list_hook_functions(self):
        """GUID: HOOKS-004 - session creation and send preserve every hook."""
        calls = []
        sent_requests = []

        def hook_a(request):
            calls.append('a')
            return request

        def hook_b(request):
            calls.append('b')
            return request

        original_send = Request.send

        def send(request, anyway=False, prefetch=None):
            sent_requests.append(request)
            dispatch_hook('pre_send', request.hooks, request)
            request.sent = True
            return True

        Request.send = send
        try:
            Session().request(
                'get',
                'http://example.com/',
                hooks={'pre_send': [hook_a, hook_b]},
            )
        finally:
            Request.send = original_send

        self.assertEqual(calls, ['a', 'b'])
        self.assertEqual(sent_requests[0].hooks['pre_send'], [hook_a, hook_b])

    def test_HOOKS_004_session_hook_event_completes_without_calling_list(self):
        """GUID: HOOKS-004 - session event consumption never calls the list."""
        calls = []

        def hook_a(args):
            calls.append('a')
            return args

        def hook_b(args):
            calls.append('b')
            return args

        session = Session(hooks={'args': [hook_a, hook_b]})
        request = session.request(
            'get', 'http://example.com/', return_response=False)

        self.assertEqual(calls, ['a', 'b'])
        self.assertEqual(request.hooks['args'], [hook_a, hook_b])
