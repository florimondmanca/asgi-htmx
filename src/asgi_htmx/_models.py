import json
from typing import Any, Optional
from urllib.parse import unquote

from ._types import Scope


class HtmxDetails:
    def __init__(self, scope: Scope) -> None:
        self._scope = scope

    def _get_header(self, name: bytes) -> Optional[str]:
        return _get_header(self._scope, name)

    def __bool__(self) -> bool:
        return self._get_header(b"HX-Request") == "true"

    @property
    def boosted(self) -> bool:
        return self._get_header(b"HX-Boosted") == "true"

    @property
    def current_url(self) -> Optional[str]:
        return self._get_header(b"HX-Current-URL")

    @property
    def history_restore_request(self) -> bool:
        return self._get_header(b"HX-History-Restore-Request") == "true"

    @property
    def prompt(self) -> Optional[str]:
        return self._get_header(b"HX-Prompt")

    @property
    def target(self) -> Optional[str]:
        return self._get_header(b"HX-Target")

    @property
    def trigger(self) -> Optional[str]:
        return self._get_header(b"HX-Trigger")

    @property
    def trigger_name(self) -> Optional[str]:
        return self._get_header(b"HX-Trigger-Name")

    @property
    def triggering_event(self) -> Any:
        value = self._get_header(b"Triggering-Event")

        if value is None:
            return None

        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return None


def _get_header(scope: Scope, key: bytes) -> Optional[str]:
    key = key.lower()
    value: Optional[str] = None
    should_unquote = False

    for k, v in scope["headers"]:
        if k.lower() == key:
            value = v.decode("latin-1")
        if k.lower() == b"%s-uri-autoencoded" % key and v == b"true":
            should_unquote = True

    if value is None:
        return None

    return unquote(value) if should_unquote else value
