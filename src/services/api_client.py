import logging
from typing import List, Dict, Literal
from aiohttp import ClientSession, ClientResponseError

logger = logging.getLogger(__name__)


class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        chat_id: int,
        response_type: Literal["json", "bytes", "text"] = "json",
        **kwargs,
    ):
        url = f"{self.base_url}{endpoint}"
        headers = {"X-Telegram-Chat-ID": str(chat_id)}

        async with ClientSession() as session:
            async with session.request(
                method, url, headers=headers, **kwargs
            ) as response:

                if response.status >= 400:
                    text = await response.text()
                    logger.warning(f"status: {response.status}. message: {text}")
                    raise ClientResponseError(
                        request_info=response.request_info,
                        history=response.history,
                        status=response.status,
                        message=text,
                    )

                match response_type:
                    case "json":
                        return await response.json()
                    case "text":
                        return await response.text()
                    case "bytes":
                        return await response.read()
                    case _:
                        raise ValueError(f"Unsupported response type: {response_type}")

    async def get(
        self,
        endpoint: str,
        chat_id: int,
        params: dict = None,
        response_type: Literal["json", "bytes", "text"] = "json",
    ) -> List[Dict] | str:

        return await self._make_request(
            "GET", endpoint, chat_id, params=params, response_type=response_type
        )

    async def post(self, endpoint: str, chat_id: int, json: dict = None):

        return await self._make_request("POST", endpoint, chat_id, json=json)

    async def put(self, endpoint: str, chat_id: int, json: dict = None):

        return await self._make_request("PUT", endpoint, chat_id, json=json)

    async def patch(self, endpoint: str, chat_id: int, json: dict = None):

        return await self._make_request("PATCH", endpoint, chat_id, json=json)

    async def delete(self, endpoint: str, chat_id: int):

        return await self._make_request("DELETE", endpoint, chat_id)
