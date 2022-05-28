from typing import Any, Literal, Protocol, overload

from ._models import HtmxDetails

try:
    from starlette.requests import Request
except ImportError:
    # Starlette not installed.
    pass
else:

    class _HtmxRequestProto(Protocol):
        @overload
        def __getitem__(self, key: Literal["htmx"]) -> HtmxDetails:
            ...

        @overload
        def __getitem__(self, key: str) -> Any:
            ...

    class HtmxRequest(_HtmxRequestProto, Request):
        pass
