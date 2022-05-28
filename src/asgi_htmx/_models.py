import json
from typing import Any, Optional
from urllib.parse import unquote

from ._types import Scope


class HtmxDetails:
    def __init__(self, scope: Scope) -> None:
        assert scope["type"] == "http"
        self._scope = scope

    def _get_header_value(self, key: bytes) -> Optional[str]:
        key = key.lower()

        value: Optional[str] = None
        should_unquote = False

        for k, v in self._scope["headers"]:
            if k.lower() == key:
                value = v.decode("latin-1")
            if k.lower() == b"%s-uri-autoencoded" % key and v == b"true":
                should_unquote = True

        if value is None:
            return None

        return unquote(value) if should_unquote else value

    def __bool__(self) -> bool:
        return self._get_header_value(b"HX-Request") == "true"

    @property
    def boosted(self) -> bool:
        return self._get_header_value(b"HX-Boosted") == "true"

    @property
    def current_url(self) -> Optional[str]:
        return self._get_header_value(b"HX-Current-URL")

    @property
    def history_restore_request(self) -> bool:
        return self._get_header_value(b"HX-History-Restore-Request") == "true"

    @property
    def prompt(self) -> Optional[str]:
        return self._get_header_value(b"HX-Prompt")

    @property
    def target(self) -> Optional[str]:
        return self._get_header_value(b"HX-Target")

    @property
    def trigger(self) -> Optional[str]:
        return self._get_header_value(b"HX-Trigger")

    @property
    def trigger_name(self) -> Optional[str]:
        return self._get_header_value(b"HX-Trigger-Name")

    @property
    def triggering_event(self) -> Any:
        value = self._get_header_value(b"Triggering-Event")
        if value is not None:
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                value = None
        return value
