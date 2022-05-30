from ._middleware import HtmxMiddleware
from ._models import HtmxDetails

try:
    from ._requests import HtmxRequest
except ImportError:  # pragma: no cover
    pass  # Starlette not installed.

__version__ = "0.1.0"

__all__ = [
    "__version__",
    "HtmxMiddleware",
    "HtmxDetails",
    "HtmxRequest",
]
