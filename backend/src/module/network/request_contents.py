import logging
import re
import xml.etree.ElementTree

from module.conf import settings
from module.models import Torrent

from .request_url import RequestURL
from .site import rss_parser

logger = logging.getLogger(__name__)


@property
def gen_filter():
    return "|".join(settings.rss.filter)


class RequestContent(RequestURL):
    async def get_torrents(
        self,
        _url: str,
        _filter: str = gen_filter,
        limit: int = None,
        retry: int = 3,
    ) -> list[Torrent]:
        feeds = await self.get_xml(_url, retry)
        if feeds:
            torrent_titles, torrent_urls, torrent_homepage = rss_parser(feeds)
            torrents: list[Torrent] = []
            for _title, torrent_url, homepage in zip(
                torrent_titles, torrent_urls, torrent_homepage
            ):
                if re.search(_filter, _title) is None:
                    torrents.append(
                        Torrent(name=_title, url=torrent_url, homepage=homepage)
                    )
            return torrents if limit is None else torrents[:limit]
        else:
            logger.error(f"[Network] Torrents list is empty: {_url}")
            return []

    async def get_xml(self, _url, retry: int = 3) -> xml.etree.ElementTree.Element:
        req = await self.get_url(_url, retry)
        if req:
            return xml.etree.ElementTree.fromstring(req.text)

    # API JSON
    async def get_json(self, _url) -> dict:
        req = await self.get_url(_url)
        if req:
            return req.json()

    async def post_data(self, _url, data: dict, files: dict[str, bytes]) -> dict:
        return await self.post_url(_url, data, files)

    async def get_html(self, _url):
        req = await self.get_url(_url)
        if req:
            return req.text

    async def get_content(self, _url):
        req = await self.get_url(_url)
        if req:
            return req.content

    async def check_connection(self, _url):
        return await self.check_url(_url)

    async def get_rss_title(self, _url):
        soup = await self.get_xml(_url)
        if soup:
            return soup.find("./channel/title").text
