from ._models import HtmxDetails
from ._types import ASGIApp, Receive, Scope, Send


class HtmxMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self._app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] in ("http", "websocket"):
            scope["htmx"] = HtmxDetails(scope)

        await self._app(scope, receive, send)
