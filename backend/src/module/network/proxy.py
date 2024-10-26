import logging
import httpx
from module.conf import settings

logger = logging.getLogger(__name__)


def set_proxy():
    auth = (
        f"{settings.proxy.username}:{settings.proxy.password}@"
        if settings.proxy.username
        else ""
    )
    if "http" in settings.proxy.type:
        proxy = (
            f"{settings.proxy.type}://{auth}{settings.proxy.host}:{settings.proxy.port}"
        )
    elif settings.proxy.type == "socks5":
        proxy = f"socks5://{auth}{settings.proxy.host}:{settings.proxy.port}"
    else:
        proxy = None
        logger.error(f"[Network] Unsupported proxy type: {settings.proxy.type}")
    return proxy


def test_proxy() -> bool:
    with httpx.Client(proxies=set_proxy()) as client:
        try:
            client.get("https://www.baidu.com")
            return True
        except httpx.ProxyError:
            logger.error(
                f"[Network] Cannot connect to proxy, please check your proxy username{settings.proxy.username} and password {settings.proxy.password}"
            )
            return False
        except httpx.ConnectError:
            logger.error(
                f"host is down, please check your proxy host {settings.proxy.host}"
            )
            return False
        except httpx.ConnectTimeout:
            logger.error(
                f"[Network] Cannot connect to proxy {settings.proxy.host}:{settings.proxy.port}"
            )
            return False


if __name__ == "__main__":
    if test_proxy():
        with httpx.Client(proxies=set_proxy()) as client:
            client.headers["User-Agent"] = (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
            )
            httpx.get("https://www.baidu.com")
            client.get("https://www.baidu.com")
