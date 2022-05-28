# examples

## Usage

Starlette:

```bash
pip install starlette uvicorn

uvicorn examples.starlette:app
```

FastAPI:

```bash
pip install fastapi uvicorn

uvicorn examples.fastapi:app
```

Quart:

```bash
pip install quart

QUART_APP=examples.quart:app quart run
```
