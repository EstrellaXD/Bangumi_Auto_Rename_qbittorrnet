import asyncio
import logging

import httpx

from module.conf import settings

from .proxy import set_proxy

logger = logging.getLogger(__name__)


class RequestURL:
    def __init__(self):
        self.header = {"user-agent": "Mozilla/5.0", "Accept": "application/xml"}
        self.proxy = set_proxy() if settings.proxy.enable else None

    async def get_url(self, url, retry=3):
        for _ in range(retry):
            try:
                req = await self.client.get(url=url)
                return req
            except httpx.TimeoutException:
                logger.debug(
                    f"[Network] Timeout. Cannot connect to {url}. Wait for 5 seconds."
                )
            except httpx.RequestError:
                logger.debug(f"[Network] Cannot connect to {url}. Wait for 5 seconds.")
            except Exception as e:
                logger.debug(f"[Network] {e}")
                logger.error(f"[Network] Cannot connect to {url}")
                break
            await asyncio.sleep(5)

    async def post_url(
        self,
        url: str,
        data: dict,
        files: dict[str, bytes] | None = None,
        retry: int = 3,
    ):
        for _ in range(retry):
            try:
                req = await self.client.post(url=url, data=data, files=files)
                return req
            except httpx.TimeoutException:
                logger.debug(
                    f"[Network] Timeout. Cannot connect to {url}. Wait for 5 seconds."
                )
            except httpx.RequestError:
                logger.debug(f"[Network] Cannot connect to {url}. Wait for 5 seconds.")
            except Exception as e:
                logger.debug(f"[Network] {e}")
                logger.error(f"[Network] Cannot connect to {url}")
                break
            await asyncio.sleep(5)

    async def check_url(self, url: str):
        if "://" not in url:
            url = f"http://{url}"
        try:
            req = await self.client.get(url=url)
            req.raise_for_status()
            return True
        except httpx.RequestError:
            logger.debug(f"[Network] Cannot connect to {url}.")
            return False

    async def __aenter__(self):
        self.client = httpx.AsyncClient(
            http2=True, proxies=self.proxy, headers=self.header, timeout=5
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
