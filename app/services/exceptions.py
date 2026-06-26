"""Service-layer exceptions, translated to HTTP responses at the router boundary."""


class ServiceError(Exception):
    """Base class for all service-layer errors."""


class NotFoundError(ServiceError):
    """Raised when a symbol, document_id, or watchlist entry cannot be found."""


class AuthenticationError(ServiceError):
    """Raised when credentials are invalid or a token cannot be verified (HTTP 401)."""


class ConflictError(ServiceError):
    """Raised when a resource already exists (e.g. company already in watchlist)."""


class ProcessingError(ServiceError):
    """Raised when document/report processing cannot proceed (HTTP 422)."""
