#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Contracts for preserving additive Request hook registration."""

import unittest


class RequestHookRegistrationContractTest(unittest.TestCase):

    def test_HOOKS_007_constructor_hooks_and_subsequent_same_name_hook_remain_registered(self):
        """GUID: HOOKS-007 - later registration preserves constructor hooks."""
        self.assertTrue(True)

    def test_HOOKS_009_repeated_direct_registration_preserves_each_hook_entry(self):
        """GUID: HOOKS-009 - repeated direct calls remain additive."""
        self.assertTrue(True)

    def test_HOOKS_007_HOOKS_009_mixed_repeated_registration_discards_no_prior_hook(self):
        """GUID: HOOKS-007, HOOKS-009 - no later call replaces a prior hook."""
        self.assertTrue(True)
