# asgi-htmx

[HTMX](https://htmx.org) integration for [ASGI](https://asgi.readthedocs.io/en/latest/) applications. Works with Starlette, FastAPI, Quart -- or any other web framework supporting ASGI that exposes the ASGI `scope`. Inspired by [django-htmx](https://github.com/adamchainz/django-htmx).

**Table of contents**

- [Installation](#installation)
- [Quickstart](#quickstart)
- [API Reference](#api-reference)

## Installation

_**NOTE**: This is alpha software -- things might break anytime. Please pin your dependencies._

```
pip install asgi-htmx==0.1.*
```

## Quickstart

First, ensure [HTMX is installed](https://htmx.org/docs/#installing).

For example, download a copy of `htmx.min.js`, add it to your [static files](https://www.starlette.io/staticfiles/), then add the script tag to your templates:

```html
<script src="{{ url_for('static', path='/js/htmx.min.js') }}" defer></script>
```

Now, install `HtmxMiddleware` onto the ASGI app:

* Using Starlette:

    ```python
    from asgi_htmx import HtmxMiddleware
    from starlette.middleware import Middleware

    app = Starlette(
        middleware=[
            ...,
            Middleware(HtmxMiddleware),
            ...,
        ],
    )

* Using FastAPI:

    ```python
    from asgi_htmx import HtmxMiddleware
    from fastapi import FastAPI

    app = FastAPI()
    app.add_middleware(HtmxMiddleware)
    ```

You can now access `scope["htmx"]` (an instance of [`HtmxDetails`](#htmxdetails)) in endpoints:

```python
from asgi_htmx import HtmxRequest as Request  # Make code editors understand `request["htmx"]`

from .resources import templates

async def home(request: Request):
    template = "home.html"
    context = {"request": request}

    if (htmx := request["htmx"]):  # Typed shortcut for `request.scope["htmx"]`
        template = "partials/items.html"
        context["boosted"] = htmx.boosted  # ...

    return templates.TemplateResponse(template, context)
```

See [examples](./examples) for full working example code.

## API Reference

### `HtmxMiddleware`

An ASGI middleware that sets `scope["htmx"]` to an instance of [`HtmxDetails`](#htmxdetails) (`scope` refers to the ASGI scope).

### `HtmxDetails`

A helper that provides shortcuts for accessing HTMX-specific [request headers](https://htmx.org/reference/#request_headers).

#### `__bool__() -> bool`

Return `True` if the request was made using HTMX (`HX-Request` is present), `False` otherwise.

#### `boosted: bool`

Mirrors the `HX-Boosted` header: `True` if the request is via an element with the [`hx-boost`](https://htmx.org/attributes/hx-boost/) attribute.

#### `current_url: str | None`

Mirrors the `HX-Current-URL` header: The current URL of the browser, or `None` for non-HTMX requests.

#### `history_restore_request: str`

Mirrors the `HX-History-Restore-Request` header: `True` if the request is for history restoration after a miss in the local history cache.

#### `prompt: str | None`

Mirrors `HX-Prompt: The user response to [`hx-prompt`](https://htmx.org/attributes/hx-prompt/) if it was used, or `None`.

#### `target: str | None`

Mirrors `HX-Target: The `id` of the target element if it exists, or `None`.

#### `trigger: str | None`

Mirrors `HX-Trigger: The `id` of the trigger element if it exists, or `None`.

#### `trigger_name: str | None`

Mirrors `HX-Trigger-Name: The `name` of the trigger element if it exists, or `None`.

#### `triggering_event: Any | None`

Mirrors `Triggering-Event`, which is set by the [event-header extension](https://htmx.org/extensions/event-header/): The deserialized JSON representation of the event that triggered the request if it exists, or `None`.

### `HtmxRequest`

For Starlette-based frameworks, when using type hints, use this instead of the standard `starlette.requests.Request` so that editors understand that `request["htmx"]` contains an `HtmxDetails` instance:

```python
from asgi_htmx import HtmxRequest as Request

async def home(request: Request):
    reveal_type(request["htmx"])  # Revealed type is 'HtmxDetails'
```

## License

MIT
