from quart import Quart, render_template, request

from asgi_htmx import HtmxDetails

app = Quart(__name__)


@app.route("/")
async def home():
    return await render_template("home.html", framework="quart")


@app.route("/result")
async def result():
    assert (htmx := HtmxDetails(request.scope))
    context = {
        "rows": [(k, getattr(htmx, k)) for k in dir(htmx) if not k.startswith("_")],
    }
    return await render_template("partials/result.html", **context)
