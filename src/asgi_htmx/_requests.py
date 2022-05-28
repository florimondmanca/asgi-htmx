from typing import Any, Literal, Protocol, overload

from ._models import HtmxDetails
from ._types import Scope

try:
    from starlette.requests import Request
except ImportError:  # pragma: no cover
    pass  # Starlette not installed.
else:

    class _HtmxScopeProto(Protocol):
        @overload
        def __getitem__(self, key: Literal["htmx"]) -> HtmxDetails:
            ...  # pragma: no cover

        @overload
        def __getitem__(self, key: str) -> Any:
            ...  # pragma: no cover

    class HtmxScope(_HtmxScopeProto, Scope):
        pass

    class HtmxRequest(Request):
        scope: HtmxScope
