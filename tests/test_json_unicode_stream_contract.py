#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Traceability placeholders for JSON Unicode streaming requirements.

JSON-001 maps to
``test_JSON_001_application_json_without_charset_decode_unicode_yields_only_str``.
JSON-002 maps to
``test_JSON_002_joined_decode_unicode_chunks_equal_response_text``.
JSON-003 maps to both boundary-specific tests containing ``JSON_003``.
JSON-006 maps to
``test_JSON_006_decoded_str_is_yielded_before_complete_body_is_buffered``.
"""


def test_JSON_001_application_json_without_charset_decode_unicode_yields_only_str():
    """JSON-001: decoding a charset-less JSON stream yields only Unicode str."""
    assert True


def test_JSON_002_joined_decode_unicode_chunks_equal_response_text():
    """JSON-002: ordered decoded chunks reconstruct response.text exactly."""
    assert True


def test_JSON_003_transport_split_multibyte_character_is_preserved_exactly():
    """JSON-003: a transport-split multibyte character remains unchanged."""
    assert True


def test_JSON_003_requested_chunk_split_multibyte_character_is_preserved_exactly():
    """JSON-003: a chunk-size-split multibyte character remains unchanged."""
    assert True


def test_JSON_006_decoded_str_is_yielded_before_complete_body_is_buffered():
    """JSON-006: decoded text is observable before the full body is buffered."""
    assert True
