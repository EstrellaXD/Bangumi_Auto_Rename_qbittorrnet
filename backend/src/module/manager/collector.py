import logging

from module.conf import settings
from module.database import Database, engine
from module.downloader import DownloadQueue
from module.models import Bangumi
from module.models.rss import RSSItem
from module.parser import TmdbParser
from module.rss import RSSEngine, RSSManager
from module.searcher import SearchTorrent

logger = logging.getLogger(__name__)


class SeasonCollector:
    def __init__(self):
        self.st = SearchTorrent()
        self.rss_engine = RSSEngine()

    

    @staticmethod
    async def subscribe_season(data: Bangumi, parser: str = "mikan"):
        """
        主要用于订阅 rss subscribe, 订阅后会自动下载
        """
        data.added = True
        data.eps_collect = True
        await RSSManager().add_rss(
            rss_link=data.rss_link,
            name=data.official_title,
            aggregate=False,
            parser=parser,
        )
        # 当 解析失败的时候, 会没有海报
        if data.poster_link is None:
            try:
                await TmdbParser.poster_parser(data)
            except Exception:
                logging.warning(f"[Engine] Fail to pull poster {data.official_title} ")

        with Database() as db:
            db.bangumi.add(data)
        # TODO: 有一点小问题是, 这里的 torrent 没有 rss_id
        result = await RSSEngine().refresh_rss(bangumi=data)
        if result:
            return True
        return False


async def eps_complete():
    # with RSSEngine() as engine:
    with Database(engine) as db:
        datas = db.bangumi.not_complete()
        if datas:
            logger.info("Start collecting full season...")
            for data in datas:
                if not data.eps_collect:
                    # collector = SeasonCollector()
                    original_rss_link = data.rss_link
                    data.rss_link = SearchTorrent().special_url(data, "mikan")
                    try:
                        await RSSEngine().refresh_rss(bangumi=data)
                        data.eps_collect = True
                        data.rss_link = original_rss_link
                        db.bangumi.update(data)
                    except Exception as e:
                        logger.error(f"[eps_complete] {e}")
            # db.bangumi.update_all(datas)


if __name__ == "__main__":
    import asyncio

    # async def subscrib_s():
    #     # t = RSSItem(url=link)
    #     return await analysis(t)

    official_title = "败犬女主太多了！"
    rss_link = "https://mikanani.me/RSS/Bangumi?bangumiId=3391&subgroupid=583"
    t = Bangumi(official_title=official_title, rss_link=rss_link)
    ans = asyncio.run(eps_complete())
    # print(ans)
