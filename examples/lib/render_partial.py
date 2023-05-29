# Inspired by: https://github.com/mikeckennedy/jinja_partials
from typing import TYPE_CHECKING, Any

import markupsafe

if TYPE_CHECKING:
    from quart import Quart
    from starlette.templating import Jinja2Templates


def register_starlette(templates: "Jinja2Templates") -> None:
    def render_partial(name: str, **context: Any) -> str:
        return markupsafe.Markup(templates.get_template(name).render(**context))

    templates.env.globals.update(render_partial=render_partial)


def register_quart(app: "Quart") -> None:
    async def render_partial(name: str, **context: Any) -> str:
        # NOTE: Quart automatically awaits function calls in its templates environment.
        html = await app.jinja_env.get_template(name).render_async(**context)
        return markupsafe.Markup(html)

    app.jinja_env.globals.update(render_partial=render_partial)
