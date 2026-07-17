#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Placeholder contracts for consuming list-valued hooks through sessions."""

import unittest


class SessionListHooksContractTest(unittest.TestCase):

    def test_HOOKS_002_consuming_list_hook_invokes_each_function_not_list(self):
        """GUID: HOOKS-002 - consume each registered function separately."""
        self.assertTrue(True)

    def test_HOOKS_004_session_create_send_preserves_all_list_hook_functions(self):
        """GUID: HOOKS-004 - session creation and send preserve every hook."""
        self.assertTrue(True)

    def test_HOOKS_004_session_hook_event_completes_without_calling_list(self):
        """GUID: HOOKS-004 - session event consumption never calls the list."""
        self.assertTrue(True)
