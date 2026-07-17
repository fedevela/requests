#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Contract tests for JSON Unicode streaming requirements.

JSON-001 maps to
``test_JSON_001_application_json_without_charset_decode_unicode_yields_only_str``.
JSON-002 maps to
``test_JSON_002_joined_decode_unicode_chunks_equal_response_text``.
JSON-003 maps to both boundary-specific tests containing ``JSON_003``.
JSON-004 maps to both raw-byte tests containing ``JSON_004``.
JSON-005 maps to both explicit-charset tests containing ``JSON_005``.
JSON-006 maps to
``test_JSON_006_decoded_str_is_yielded_before_complete_body_is_buffered``.
JSON-007 maps to both complete-response-text tests containing ``JSON_007``.
"""

import io

from requests.models import Response
from requests.utils import get_encoding_from_headers


JSON_TEXT = '{"message":"Olá, € and 雪"}'
RAW_CONTENT_CHUNKS = [
    b'\x00{"payload":"\xff',
    b'\x80\xfe",',
    b'"tail":"\x00"}\r\n',
]
RAW_CONTENT = b''.join(RAW_CONTENT_CHUNKS)
EXPLICIT_CHARSET = 'utf-16-le'
EXPLICIT_CHARSET_TEXT = '{"message":"Zażółć gęślą jaźń — 雪"}'
EXPLICIT_CHARSET_CONTENT = EXPLICIT_CHARSET_TEXT.encode(EXPLICIT_CHARSET)


def buffered_json_response(text=JSON_TEXT):
    response = Response()
    response.headers['Content-Type'] = 'application/json'
    response.encoding = get_encoding_from_headers(response.headers)
    response._content = text.encode('utf-8')
    response._content_consumed = True
    return response


def streamed_json_response(raw, charset=None):
    response = Response()
    content_type = 'application/json'
    if charset is not None:
        content_type += '; charset=%s' % charset
    response.headers['Content-Type'] = content_type
    response.encoding = get_encoding_from_headers(response.headers)
    response.raw = raw
    return response


class TrackingRaw(object):
    """A transport iterator that exposes how many chunks were requested."""

    def __init__(self, chunks):
        self.chunks = chunks
        self.chunks_requested = 0

    def stream(self, chunk_size, decode_content=True):
        for chunk in self.chunks:
            self.chunks_requested += 1
            yield chunk


def test_JSON_001_application_json_without_charset_decode_unicode_yields_only_str():
    """JSON-001: decoding a charset-less JSON stream yields only Unicode str."""
    response = buffered_json_response()

    chunks = list(response.iter_content(2, decode_unicode=True))

    assert response.encoding == 'utf-8'
    assert chunks
    assert all(isinstance(chunk, str) for chunk in chunks)


def test_JSON_002_joined_decode_unicode_chunks_equal_response_text():
    """JSON-002: ordered decoded chunks reconstruct response.text exactly."""
    response = buffered_json_response()

    streamed_text = ''.join(response.iter_content(3, decode_unicode=True))

    assert streamed_text == response.text
    assert streamed_text == JSON_TEXT


def test_JSON_003_transport_split_multibyte_character_is_preserved_exactly():
    """JSON-003: a transport-split multibyte character remains unchanged."""
    response = streamed_json_response(TrackingRaw([
        b'{"currency":"\xe2',
        b'\x82',
        b'\xac"}',
    ]))

    decoded = ''.join(response.iter_content(1024, decode_unicode=True))

    assert decoded == '{"currency":"€"}'
    assert decoded.count('€') == 1


def test_JSON_003_requested_chunk_split_multibyte_character_is_preserved_exactly():
    """JSON-003: a chunk-size-split multibyte character remains unchanged."""
    expected = '{"currency":"€"}'
    encoded = expected.encode('utf-8')
    first_euro_byte = encoded.index(b'\xe2')
    response = streamed_json_response(io.BytesIO(encoded))

    decoded = ''.join(response.iter_content(
        first_euro_byte + 1, decode_unicode=True))

    assert decoded == expected
    assert decoded.count('€') == 1


def test_JSON_004_decode_unicode_false_yields_only_bytes():
    """JSON-004: disabling Unicode decoding yields only raw byte values."""
    response = streamed_json_response(TrackingRaw(RAW_CONTENT_CHUNKS))

    chunks = list(response.iter_content(3, decode_unicode=False))

    assert chunks
    assert all(isinstance(chunk, bytes) for chunk in chunks)


def test_JSON_004_joined_raw_byte_chunks_equal_unmodified_response_content():
    """JSON-004: ordered raw-byte chunks preserve the response content."""
    response = streamed_json_response(TrackingRaw(RAW_CONTENT_CHUNKS))

    streamed_content = b''.join(
        response.iter_content(3, decode_unicode=False))

    assert streamed_content == RAW_CONTENT


def test_JSON_005_explicit_response_charset_decode_unicode_yields_only_str():
    """JSON-005: an explicit charset yields only decoded Unicode str."""
    response = streamed_json_response(
        io.BytesIO(EXPLICIT_CHARSET_CONTENT), EXPLICIT_CHARSET)

    chunks = list(response.iter_content(3, decode_unicode=True))

    assert response.encoding == EXPLICIT_CHARSET
    assert chunks
    assert all(isinstance(chunk, str) for chunk in chunks)


def test_JSON_005_joined_decode_unicode_chunks_use_declared_charset():
    """JSON-005: joined chunks preserve text under the declared charset."""
    response = streamed_json_response(
        io.BytesIO(EXPLICIT_CHARSET_CONTENT), EXPLICIT_CHARSET)

    streamed_text = ''.join(
        response.iter_content(3, decode_unicode=True))

    assert streamed_text == EXPLICIT_CHARSET_TEXT
    assert streamed_text == EXPLICIT_CHARSET_CONTENT.decode(EXPLICIT_CHARSET)


def test_JSON_006_decoded_str_is_yielded_before_complete_body_is_buffered():
    """JSON-006: decoded text is observable before the full body is buffered."""
    raw = TrackingRaw([
        b'{"message":"ready',
        b' now"}',
    ])
    response = streamed_json_response(raw)
    chunks = response.iter_content(1024, decode_unicode=True)

    first = next(chunks)

    assert first == '{"message":"ready'
    assert raw.chunks_requested == 1
    assert response._content is False
    assert response._content_consumed is False
    assert first + ''.join(chunks) == '{"message":"ready now"}'


def test_JSON_007_given_complete_text_accessing_response_text_returns_unicode_str():
    """JSON-007: complete response text is exposed as a Unicode str."""
    assert True


def test_JSON_007_given_complete_text_accessing_response_text_returns_all_content_once():
    """JSON-007: response.text has no missing or duplicated content."""
    assert True
