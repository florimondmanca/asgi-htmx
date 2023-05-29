from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from asgi_htmx import HtmxMiddleware
from asgi_htmx import HtmxRequest as Request

from .common import HERE, make_table

app = FastAPI()
app.mount("/static", StaticFiles(directory=HERE / "static"), name="static")
app.add_middleware(HtmxMiddleware)

templates = Jinja2Templates(directory=HERE / "templates")


@app.get("/", name="home")
async def home(request: Request) -> Response:
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/result", name="result")
async def result(request: Request) -> Response:
    assert (htmx := request.scope["htmx"])
    template = "partials/result.html"
    context = {"request": request, "table": make_table(htmx)}
    return templates.TemplateResponse(template, context)
