# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## 0.1.0 - 2022-05-30

_Initial release_

## Added

* Add `HtmxDetails` that facilitates working with `HX-*` request headers.
* Add `HtmxMiddleware` that automatically adds an `HtmxDetails` instance as `scope["htmx"]`.
* Add `HtmxRequest` that facilitates type hinting `request.scope["htmx"]` in Starlette-based frameworks.
