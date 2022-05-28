from ._middleware import HtmxMiddleware
from ._models import HtmxDetails

try:
    from ._requests import HtmxRequest
except ImportError:
    pass

__version__ = "0.0.1"

__all__ = [
    "__version__",
    "HtmxMiddleware",
    "HtmxDetails",
    "HtmxRequest",
]
