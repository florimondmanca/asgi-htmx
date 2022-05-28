from pathlib import Path

from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from asgi_htmx import HtmxMiddleware
from asgi_htmx import HtmxRequest as Request

HERE = Path(__file__).parent

templates = Jinja2Templates(directory=HERE / "templates")

app = FastAPI()
app.mount("/static", StaticFiles(directory=HERE / "static"), name="static")
app.add_middleware(HtmxMiddleware)


@app.get("/", name="home")
async def home(request: Request) -> Response:
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/result", name="result")
async def result(request: Request) -> Response:
    assert (htmx := request["htmx"])
    template = "partials/result.html"
    context = {
        "request": request,
        "rows": [(k, getattr(htmx, k)) for k in dir(htmx) if not k.startswith("_")],
    }
    return templates.TemplateResponse(template, context)
