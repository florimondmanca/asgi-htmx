import httpx
import lxml
import pytest

pytest.importorskip("quart")


@pytest.mark.asyncio
async def test_example_quart() -> None:
    from examples.quart import app

    async with httpx.AsyncClient(app=app) as client:
        response = await client.get("http://testserver")
        html = lxml.html.fromstring(response.text)
        button = html.xpath("//button")[0]
        assert button
        assert response.status_code == 200
