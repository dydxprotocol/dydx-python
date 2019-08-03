
class DydxError(Exception):
    """Base error class for all exceptions raised in this library.
    Will never be raised naked; more specific subclasses of this exception will
    be raised when appropriate."""


class DydxAPIError(DydxError):
    def __init__(self, response):
        self.status_code = response.status_code
        try:
            self.msg = response.json()
        except ValueError:
            self.msg = response.text
        self.response = response
        self.request = getattr(response, 'request', None)

    def __str__(self):
        return 'DydxAPIError(status_code=%s)(response=%s)' \
            % (self.status_code, self.msg)
