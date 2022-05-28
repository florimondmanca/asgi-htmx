import httpx
import pytest
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.responses import JSONResponse, Response
from starlette.routing import Route

from asgi_htmx import HtmxDetails, HtmxMiddleware
from asgi_htmx import HtmxRequest as Request


async def index(request: Request) -> Response:
    htmx = request.scope["htmx"]
    assert isinstance(htmx, HtmxDetails)
    data = {
        "__bool__": bool(htmx),
        "boosted": htmx.boosted,
        "current_url": htmx.current_url,
        "history_restore_request": htmx.history_restore_request,
        "prompt": htmx.prompt,
        "target": htmx.target,
        "trigger": htmx.trigger,
        "trigger_name": htmx.trigger_name,
        "triggering_event": htmx.triggering_event,
    }
    return JSONResponse(data)


app = Starlette(
    routes=[Route("/", index)],
    middleware=[Middleware(HtmxMiddleware)],
)


@pytest.mark.asyncio
async def test_default() -> None:
    async with httpx.AsyncClient(app=app) as client:
        response = await client.get("http://testserver/")
        data = response.json()
        assert data["__bool__"] is False
        assert data["boosted"] is False
        assert data["current_url"] is None
        assert data["history_restore_request"] is False
        assert data["prompt"] is None
        assert data["target"] is None
        assert data["trigger"] is None
        assert data["trigger_name"] is None
        assert data["triggering_event"] is None


@pytest.mark.asyncio
async def test_bool_set() -> None:
    async with httpx.AsyncClient(app=app) as client:
        response = await client.get(
            "http://testserver/", headers={"HX-Request": "true"}
        )
        data = response.json()
        assert data["__bool__"] is True


@pytest.mark.asyncio
async def test_boosted_set() -> None:
    async with httpx.AsyncClient(app=app) as client:
        response = await client.get(
            "http://testserver/", headers={"HX-Boosted": "true"}
        )
        data = response.json()
        assert data["boosted"] is True


@pytest.mark.asyncio
async def test_current_url_set() -> None:
    async with httpx.AsyncClient(app=app) as client:
        response = await client.get(
            "http://testserver/",
            headers={"HX-Current-URL": "https://example.com"},
        )
        data = response.json()
        assert data["current_url"] == "https://example.com"


@pytest.mark.asyncio
async def test_current_url_set_urlencoded() -> None:
    async with httpx.AsyncClient(app=app) as client:
        response = await client.get(
            "http://testserver/",
            headers={
                "HX-Current-URL": "https%3A%2F%2Fexample.com%2F%3F",
                "HX-Current-URL-URI-AutoEncoded": "true",
            },
        )
        data = response.json()
        assert data["current_url"] == "https://example.com/?"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "value, result",
    [
        ("false", False),
        ("true", True),
    ],
)
async def test_history_restore_request(value: str, result: bool) -> None:
    async with httpx.AsyncClient(app=app) as client:
        response = await client.get(
            "http://testserver/",
            headers={"HX-History-Restore-Request": value},
        )
        data = response.json()
        assert data["history_restore_request"] is result


@pytest.mark.asyncio
async def test_prompt_set() -> None:
    async with httpx.AsyncClient(app=app) as client:
        response = await client.get(
            "http://testserver/", headers={"HX-Prompt": "Yes, please"}
        )
        data = response.json()
        assert data["prompt"] == "Yes, please"


@pytest.mark.asyncio
async def test_target_set() -> None:
    async with httpx.AsyncClient(app=app) as client:
        response = await client.get(
            "http://testserver/", headers={"HX-Target": "clickme"}
        )
        data = response.json()
        assert data["target"] == "clickme"


@pytest.mark.asyncio
async def test_trigger_set() -> None:
    async with httpx.AsyncClient(app=app) as client:
        response = await client.get(
            "http://testserver/", headers={"HX-Trigger": "click"}
        )
        data = response.json()
        assert data["trigger"] == "click"


@pytest.mark.asyncio
async def test_trigger_name_set() -> None:
    async with httpx.AsyncClient(app=app) as client:
        response = await client.get(
            "http://testserver/", headers={"HX-Trigger-Name": "email"}
        )
        data = response.json()
        assert data["trigger_name"] == "email"


@pytest.mark.asyncio
async def test_triggering_event_bad_json() -> None:
    async with httpx.AsyncClient(app=app) as client:
        response = await client.get(
            "http://testserver/", headers={"Triggering-Event": "{"}
        )
        data = response.json()
        assert data["triggering_event"] is None


@pytest.mark.asyncio
async def test_triggering_event() -> None:
    async with httpx.AsyncClient(app=app) as client:
        response = await client.get(
            "http://testserver/",
            headers={
                "Triggering-Event": "%7B%22target%22%3A%20null%7D",
                "Triggering-Event-URI-AutoEncoded": "true",
            },
        )
        data = response.json()
        assert data["triggering_event"] == {"target": None}
