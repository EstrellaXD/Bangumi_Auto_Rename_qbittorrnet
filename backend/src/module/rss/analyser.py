import logging
import re

from module.conf import settings
from module.database import Database, engine
from module.models import Bangumi, RSSItem, Torrent
from module.parser import MikanParser, RawParser, TmdbParser

logger = logging.getLogger(__name__)


class RSSAnalyser:
    def __init__(self, _engine=engine) -> None:
        self.engine = _engine

    @staticmethod
    async def official_title_parser(bangumi: Bangumi, parser: str, torrent: Torrent):
        if parser == "mikan":
            try:
                parsered_bangumi = await MikanParser().parser(torrent.homepage)
                bangumi.poster_link, bangumi.official_title = (
                    parsered_bangumi.poster_link,
                    parsered_bangumi.official_title,
                )
            except AttributeError:
                logger.warning("[Parser] Mikan torrent has no homepage info.")
        # else rss.parser == "tmdb":
        else:
            parsered_bangumi = await TmdbParser.parser(
                bangumi.official_title, bangumi.season, settings.rss_parser.language
            )
            # if parsered_bangumi porperty is not default value, update bangumi
            # FIXME: 如果解析出来的属性是默认值，则不更新
            bangumi.official_title = parsered_bangumi.official_title
            bangumi.year = parsered_bangumi.year
            bangumi.season = parsered_bangumi.season
            bangumi.poster_link = parsered_bangumi.poster_link
        # else:
        #     pass
        bangumi.official_title = re.sub(r"[/:.\\]", " ", bangumi.official_title)

    async def torrent_to_data(self, torrent: Torrent, rss: RSSItem) -> Bangumi | None:
        """
        parse torrent name to bangumi
        filter 在 RawParser 中设置
        """
        if (
            bangumi := RawParser().parser(raw=torrent.name)
        ) and bangumi.official_title != "official_title":
            await self.official_title_parser(
                bangumi=bangumi, parser=rss.parser, torrent=torrent
            )
            bangumi.rss_link = rss.url
            return bangumi

    def torrent_to_bangumi(self, torrent: Torrent, rss_item: RSSItem) -> Bangumi | None:
        """
        find bangumi from database by torrent name and rss link
        """
        # print(f"torrent_to_bangumi {torrent.name} {rss_item.url}")
        with Database(self.engine) as database:
            matched_bangumi = database.bangumi.match_torrent(
                torrent_name=torrent.name,
                rss_link=rss_item.url,
                aggrated=rss_item.aggregate,
            )
        if matched_bangumi:
            return matched_bangumi
        return None
