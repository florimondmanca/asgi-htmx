from pathlib import Path

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.responses import Response
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from asgi_htmx import HtmxMiddleware
from asgi_htmx import HtmxRequest as Request

HERE = Path(__file__).parent
static = StaticFiles(directory=HERE / "static")
templates = Jinja2Templates(directory=HERE / "templates")


async def home(request: Request) -> Response:
    return templates.TemplateResponse("home.html", {"request": request})


async def result(request: Request) -> Response:
    assert (htmx := request["htmx"])
    template = "partials/result.html"
    context = {
        "request": request,
        "rows": [(k, getattr(htmx, k)) for k in dir(htmx) if not k.startswith("_")],
    }
    return templates.TemplateResponse(template, context)


app = Starlette(
    routes=[
        Mount("/static", static, name="static"),
        Route("/", home, name="home"),
        Route("/result", result, name="result"),
    ],
    middleware=[Middleware(HtmxMiddleware)],
)
