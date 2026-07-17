# -*- coding: utf-8 -*-

"""
requests.hooks
~~~~~~~~~~~~~~

This module provides the capabilities for the Requests hooks system.

Available hooks:

``args``:
    A dictionary of the arguments being sent to Request().

``pre_request``:
    The Request object, directly after being created.

``pre_send``:
    The Request object, directly before being sent.

``post_request``:
    The Request object, directly after being sent.

``response``:
    The response generated from a Request.

"""


HOOKS = ('args', 'pre_request', 'pre_send', 'post_request', 'response')


def dispatch_hook(key, hooks, hook_data):
    """Dispatches a hook dictionary on a given piece of data."""

    # Pseudocode -- GUID: HOOKS-002
    # INPUT: hook event name, configured event-to-hook mapping, event data.
    # NORMALIZE a missing mapping to an empty mapping.
    # IF the event name has no configured value, RETURN the event data unchanged.
    # OTHERWISE, read the configured value without invoking it.
    # IF that value is one callable, treat it as a one-entry sequence.
    # OTHERWISE, treat it as the sequence of separately registered callables.
    # FOR EACH callable in sequence order:
    #     invoke the callable with the current event data, never the sequence;
    #     IF the callable returns replacement data, make it current for the
    #     next callable; OTHERWISE retain the current event data.
    #     IF invocation fails, propagate that failure and stop consumption.
    # RETURN the final current event data after every callable completes.
    hooks = hooks or dict()

    if key in hooks:
        hooks = hooks.get(key)

        if hasattr(hooks, '__call__'):
            hooks = [hooks]

        for hook in hooks:
            _hook_data = hook(hook_data)
            if _hook_data is not None:
                hook_data = _hook_data


    return hook_data
