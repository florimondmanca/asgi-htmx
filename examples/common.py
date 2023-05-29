from pathlib import Path
from typing import Any

HERE = Path(__file__).parent


def make_table(obj: Any) -> list:
    return [
        {"name": name, "value": getattr(htmx, name)}
        for name in dir(obj)
        if not name.startswith("_")
    ]
