import asyncio
import json
from collections.abc import AsyncGenerator
from typing import TypeAlias

from module.conf import settings
from module.models import Bangumi, RSSItem, Torrent
from module.network import RequestContent
from module.parser.title_parser import RawParser
from module.rss import RSSAnalyser, RSSRefresh
from module.searcher.provider import search_url

SEARCH_KEY = [
    "group_name",
    "title_raw",
    "season_raw",
    "subtitle",
    "source",
    "dpi",
]

BangumiJSON: TypeAlias = str


class SearchTorrent:
    def __init__(self) -> None:
        self.req = RequestContent
        self.analyser = RSSAnalyser()

    async def search_torrents(self, rss_item: RSSItem) -> list[Torrent]:
        # 主要是想借用一下 filter, 从 rss 拿 torrents
        bangumi = Bangumi(
            filter="|".join(settings.rss_parser.filter),
            rss_link=rss_item.url,
        )
        bangumi_torrents = RSSRefresh(bangumi=bangumi)
        await bangumi_torrents.refresh()
        if bangumi.official_title in bangumi_torrents.bangumi_torrents:
            return bangumi_torrents.bangumi_torrents[bangumi.official_title].torrents
        return []

    async def analyse_keyword(
        self, keywords: list[str], site: str = "mikan", limit: int = 7
    ) -> AsyncGenerator[BangumiJSON, None]:
        rss_item = search_url(site, keywords)
        torrents = await self.search_torrents(rss_item)
        exist_list = []
        tasks = []

        for torrent in torrents:
            if len(exist_list) >= limit:
                break
            if new_bangumi := RawParser().parser(torrent.name):
                # 检查是否已经存在, 对于一个 bangumi 来说, 组和动漫一致就可以认为是一个
                new_str = f"{new_bangumi.title_raw}{new_bangumi.group_name}"
                if new_str not in exist_list:
                    task = asyncio.create_task(
                        self.analyser.torrent_to_data(torrent=torrent, rss=rss_item)
                    )
                    tasks.append(task)
                    exist_list.append(new_str)

        while tasks:
            done, tasks = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            for task in done:
                try:
                    bangumi = await task
                    special_link = self.special_url(bangumi, site).url

                    if special_link not in exist_list:
                        bangumi.rss_link = special_link
                        exist_list.append(special_link)

                        yield {
                            "event": "message",
                            "data": json.dumps(bangumi.dict(), separators=(",", ":")),
                        }

                except Exception:
                    continue

    @staticmethod
    def special_url(data: Bangumi, site: str) -> RSSItem:
        """
        根据 bangumi 的属性, 生成一个 rss_item
        """
        keywords = [getattr(data, key) for key in SEARCH_KEY if getattr(data, key)]
        url = search_url(site, keywords)
        return url


if __name__ == "__main__":
    import asyncio

    ans = asyncio.run(SearchTorrent().analyse_keyword(["败犬女主"]))
    for _ in ans:
        print(json.loads(_))
