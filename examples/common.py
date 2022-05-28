from pathlib import Path

from asgi_htmx import HtmxDetails

HERE = Path(__file__).parent


def make_table(htmx: HtmxDetails) -> list:
    return [
        {"name": name, "value": getattr(htmx, name)}
        for name in dir(htmx)
        if not name.startswith("_")
    ]
