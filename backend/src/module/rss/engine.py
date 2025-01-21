import asyncio
import logging
import re
from abc import abstractmethod

from typing_extensions import override

from module.database import Database, engine
from module.downloader import DownloadQueue
from module.models import Bangumi, RSSItem, Torrent
from module.network import RequestContent
from module.rss.analyser import RSSAnalyser

logger = logging.getLogger(__name__)


class RssBase:
    """
    实现一些 rss 的通用方法, 获取 rss url 对应的 torrents
    当传入 bangumi 时, 会使用 bangumi 的 rss_link 作为 url
    Attributes:
        torrent_cache (list[Torrent]): The cache of torrents.
        rss_item (RSSItem): The rss item.
        bangumi (Bangumi | None): The bangumi item.
    会用到 rss 的地方一共有 3 个
    1. 日常的刷新, 这时候只有 rss_item, 没有 bangumi
    2. 订阅, 这时候没有 rss_item, 有 bangumi
    3. 收集, 这时候没有 rss_item, 有 bangumi,但 不把 bangumi 放到 database 中
    4. eps, 有 rss_item, 有 bangumi
    5. 搜索, 有 rss_item
    当有 bangumi 时, 会使用 bangumi 的 rss_link 作为 url
    """

    def __init__(
        self,
        rss_item: RSSItem | None = None,
        bangumi: Bangumi | None = None,
        _engine=engine,
    ) -> None:
        if not rss_item and not bangumi:
            raise ValueError("rss_item and bangumi can't be None at the same time")
        self.analyser:RSSAnalyser = RSSAnalyser(_engine)
        self.rss_item = rss_item
        self.bangumi = bangumi
        self.bangumi_torrents = {}
        if self.bangumi:
            self.url:str = self.bangumi.rss_link
        elif self.rss_item:
            self.url:str = self.rss_item.url

    async def _get_torrents(self, url: str) -> list[Torrent]:
        async with RequestContent() as req:
            torrents = await req.get_torrents(url)
        logging.debug(f"[RSS ENGINE] from {self.url} get {len(torrents)}")
        with Database() as database:
            new_torrents = database.torrent.check_new(torrents)
        return new_torrents

    async def pull_rss(self) -> list[Torrent]:
        """拉取 rss_item 对应的 torrents"""
        torrents = await self._get_torrents(self.url)
        # Add RSS ID
        if self.rss_item:
            for torrent in torrents:
                torrent.rss_id = self.rss_item.id
        return torrents

    async def refresh(self):
        """
        刷新 rss , 将 torrent 转为 bangumi, 返回一个 list[(bangumi,[torrent])]
        """
        pass


class RSSRefresh(RssBase):
    """
    刷新 rss 的 torrent
    """

    async def refresh(self):
        # 对一个 rss_item 做一个假设, 认为一个 rss_link 里面 一部动漫只有一季
        # 由于无法知道当前的 rss 里面是否 bangumi 是否在,所以单个 rss 中能线性处理
        # 这样 相同的 official_title 就可以认为是一个动漫, 用 official_title 作为 key
        # 对于 collect and subscribe , 只有 bangumi, 唯一的区别是 subscribe 会 add 到 database
        # 日常的是只有 rss_item, 没有 bangumi
        # 整体流程是, 先拉取 rss_item 对应的 torrents
        # 如果 self.bangumi 为空, 则去 database 中找, 如果 database 中没有, 则进行一次解析
        # 如果 self.bangumi 不为空, 则将 torrents 放到 bangumi_torrents 中, 对应为 搜索, 订阅, 收集, 非聚合

        torrents = await self.pull_rss()
        for torrent in torrents:
            # 如果 bangumi 为空, 更新 bangumi
            if not self.bangumi:
                # 先从数据库中找, 如果数据库中没有, 更新一下 database
                bangumi = self.analyser.torrent_to_bangumi(torrent, self.rss_item)
                if not bangumi:
                    # 如果数据库中没有, 进行一次解析
                    bangumi = await self.analyser.torrent_to_data(
                        torrent, self.rss_item
                    )
                    # TODO: 不一定在这更新
                    with Database(engine) as database:
                        database.bangumi.add(bangumi)
                if bangumi:
                    if not self.rss_item.aggregate:
                        # 如果 不是聚合的, 则更新 bangumi
                        # 这样就可以避免多余的请求
                        self.bangumi = bangumi
                    title = bangumi.official_title
                    if title not in self.bangumi_torrents:
                        self.bangumi_torrents[title] = TorrentBangumi(bangumi)
                    else:
                        # TODO: bangumi_torrents 中如果已经存在, 则更新 bangumi
                        pass
                    self.bangumi_torrents[title].append(torrent)
            else:
                # 先抓一下poster_link, 然后save, refresh_rss
                if self.bangumi.official_title not in self.bangumi_torrents:
                    self.bangumi_torrents[self.bangumi.official_title] = TorrentBangumi(
                        self.bangumi
                    )
                self.bangumi_torrents[self.bangumi.official_title].append(torrent)


class TorrentBangumi:
    """一个bangumi 对应的 list[Torrent]
    有俩种情况会用到这个

    Attributes:
        torrent: list[Torrent]
        bangumi: Bangumi
    """

    def __init__(self, bangumi_item: Bangumi) -> None:
        self.torrents = []
        self.bangumi = bangumi_item
        self.filter = self.bangumi.filter.replace(",", "|")

    def append(self, torrent_item: Torrent):
        if not self.filter or not re.search(self.filter, torrent_item.name):
            torrent_item.bangumi_id = self.bangumi.id
            self.torrents.append(torrent_item)

    def __len__(self) -> int:
        return len(self.torrents)

    def __getitem__(self, idx):
        return self.torrents[idx]

    def __str__(self) -> str:
        torrents_str = [torrent.name for torrent in self.torrents]
        return f"{self.bangumi.official_title} \n{self.filter}\n{torrents_str}"

    def __repr__(self) -> str:
        return self.__str__()


class RSSEngine:
    """要完成
    1. 将 torrent_item 转为bangumi
    2. rss_item 转为 torrent_item
    3. 发送到 Download_queue
    4. torrent 找到bangumi

    5. collect 有 rss_item,无bangumi?
    collect 就更麻烦了, rss_item 是没有的,不好找bangumi, bangumi没有不好改名
    这个到是好解决, bangumi 隐藏一下到是也能用

    6. subscribe 有 rss_item,有bangumi
    subscribe 只用refresh一下自己就好了

    7. eps 有 rss_item,有bangumi
    eps 是没有 保存rss_item的,主要是eps的rss和保存的rss不一致,不好找bangumi

    放弃
    8. 一个 rss cache , dict[rss_link,list[torrent_item], 到也不用太复杂, RSS都从 Engine 拿
    内部维护一个就好了,如果有就说明这段时间请求过,

    9. 主要是用于整体刷新, 小的 eps 之类的用 RssRefresh

    10. 聚合的要先更新一遍到 database 中

    """

    def __init__(self, _engine=engine) -> None:
        self.engine = _engine
        self.queue = DownloadQueue()

    def get_active_rss(self) -> list[RSSItem]:
        """获取所有活跃的rss"""
        with Database(self.engine) as database:
            rss_items = database.rss.search_active()
        return rss_items

    async def refresh_rss(
        self,
        rss_item: RSSItem | None = None,
        bangumi: Bangumi | None = None,
    ):
        """刷新一个rss"""
        refresh = RSSRefresh(rss_item, bangumi)
        await refresh.refresh()
        if rss_item:
            logger.info(f"[RSS] refresh {rss_item.url}")
        if bangumi:
            logger.info(f"[RSS] refresh {bangumi.official_title}")
        for value in refresh.bangumi_torrents.values():
            await self.queue.add_torrents(value.torrents, value.bangumi)

    async def refresh_all(self):
        """刷新所有rss"""
        tasks = []
        rss_items = self.get_active_rss()
        for rss_item in rss_items:
            tasks.append(self.refresh_rss(rss_item))
        await asyncio.gather(*tasks)


if __name__ == "__main__":

    async def test():
        test_rss = RSSItem(
            url="https://mikanani.me/RSS/Bangumi?bangumiId=3439&subgroupid=1207"
        )
        test_refresh = RSSRefresh(rss_item=test_rss)
        await test_refresh.refresh()
        print(test_refresh.bangumi_torrents)

    async def test_engine():
        test_engine = RSSEngine()
        await test_engine.refresh_all()

    asyncio.run(test_engine())
    # asyncio.run(test())
    # test_bangumi = Bangumi(official_title="test")
    # test_dict = {test_bangumi: []}
    # test_bangumi2 = Bangumi(official_title="test", rule_name="2")
    # test_dict[test_bangumi2].append(Torrent(url="testlink"))
    # print(test_dict)
    # test_bangumi = Bangumi(official_title="test")
    # test_torrent = Torrent(url="testlin")
    # test_class = TorrentBangumi(test_bangumi)
    # test_class.append(test_torrent)
    # print( len(test_class))
    # print(platform.system())
