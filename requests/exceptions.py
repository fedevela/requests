# -*- coding: utf-8 -*-

"""
requests.exceptions
~~~~~~~~~~~~~~~~~~~

This module contains the set of Requests' exceptions.

"""
from .packages.urllib3.exceptions import HTTPError as BaseHTTPError


class RequestException(IOError):
    """There was an ambiguous exception that occurred while handling your
    request."""

    def __init__(self, *args, **kwargs):
        """
        Initialize RequestException with `request` and `response` objects.
        """
        response = kwargs.pop('response', None)
        self.response = response
        self.request = kwargs.pop('request', None)
        if (response is not None and not self.request and
                hasattr(response, 'request')):
            self.request = self.response.request
        super(RequestException, self).__init__(*args, **kwargs)


class HTTPError(RequestException):
    """An HTTP error occurred."""


class ConnectionError(RequestException):
    """A Connection error occurred."""


class ProxyError(ConnectionError):
    """A proxy error occurred."""


class SSLError(ConnectionError):
    """An SSL error occurred."""


# GUID: EXC-002, EXC-003, EXC-004, EXC-005, EXC-006 - Requests owns this
# public timeout contract and its diagnostic, hierarchy, and termination
# guarantees.
# HTTPAdapter.send is the single translation seam for direct and proxy urllib3
# failures: classified failures target the existing subclasses below, while
# unclassified urllib3 timeouts target Timeout itself. The adapter, rather than
# callers or vendored urllib3, owns selection of the public Requests type.
class Timeout(RequestException):
    """The request timed out.

    Catching this error will catch both
    :exc:`~requests.exceptions.ConnectTimeout` and
    :exc:`~requests.exceptions.ReadTimeout` errors.
    """


class ConnectTimeout(ConnectionError, Timeout):
    """The request timed out while trying to connect to the remote server.

    Requests that produced this error are safe to retry.
    """


class ReadTimeout(Timeout):
    """The server did not send any data in the allotted amount of time."""


class URLRequired(RequestException):
    """A valid URL is required to make a request."""


class TooManyRedirects(RequestException):
    """Too many redirects."""


class MissingSchema(RequestException, ValueError):
    """The URL schema (e.g. http or https) is missing."""


class InvalidSchema(RequestException, ValueError):
    """See defaults.py for valid schemas."""


class InvalidURL(RequestException, ValueError):
    """ The URL provided was somehow invalid. """


class ChunkedEncodingError(RequestException):
    """The server declared chunked encoding but sent an invalid chunk."""


# GUID: EXC-001, EXC-004, EXC-005, EXC-006 - Requests owns this public
# response-decoding contract and its diagnostic, hierarchy, and termination
# guarantees.
# Response.iter_content is the adapter seam from urllib3 DecodeError to this
# exception; the vendored urllib3 layer remains independent of Requests and
# callers need no dependency on its exception types.
class ContentDecodingError(RequestException, BaseHTTPError):
    """Failed to decode response content"""


class StreamConsumedError(RequestException, TypeError):
    """The content for this response was already consumed"""


class RetryError(RequestException):
    """Custom retries logic failed"""
