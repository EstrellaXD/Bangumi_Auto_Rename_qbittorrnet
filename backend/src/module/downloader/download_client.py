import logging

from module.conf import settings
from module.models import Bangumi, Torrent
from module.network import RequestContent
from module.utils import torrent_hash

from .path import TorrentPath

logger = logging.getLogger(__name__)


class DownloadClient(TorrentPath):
    def __init__(self):
        super().__init__()
        self.client = self.__getClient()
        self.authed = False

    @staticmethod
    def __getClient():
        # TODO 多下载器支持
        type = settings.downloader.type
        host = settings.downloader.host
        username = settings.downloader.username
        password = settings.downloader.password
        ssl = settings.downloader.ssl
        if type == "qbittorrent":
            from .client.qb_downloader import QbDownloader

            return QbDownloader(host, username, password, ssl)
        else:
            logger.error(f"[Downloader] Unsupported downloader type: {type}")
            raise Exception(f"Unsupported downloader type: {type}")

    def __enter__(self):
        if not self.authed:
            self.auth()
        else:
            logger.error("[Downloader] Already authed.")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.authed:
            self.client.logout()
            self.authed = False

    def auth(self):
        self.authed = self.client.auth()
        if self.authed:
            logger.debug("[Downloader] Authed.")
        else:
            logger.error("[Downloader] Auth failed.")

    def check_host(self):
        return self.client.check_host()

    def init_downloader(self):
        prefs = {
            "rss_auto_downloading_enabled": True,
            "rss_max_articles_per_feed": 500,
            "rss_processing_enabled": True,
            "rss_refresh_interval": 30,
        }
        self.client.prefs_init(prefs=prefs)
        try:
            self.client.add_category("BangumiCollection")
        except Exception:
            logger.debug("[Downloader] Cannot add new category, maybe already exists.")
        if settings.downloader.path == "":
            prefs = self.client.get_app_prefs()
            settings.downloader.path = self._join_path(prefs["save_path"], "Bangumi")

    def set_rule(self, data: Bangumi):
        data.rule_name = self._rule_name(data)
        data.save_path = self._gen_save_path(data)
        rule = {
            "enable": True,
            "mustContain": data.title_raw,
            "mustNotContain": "|".join(data.filter),
            "useRegex": True,
            "episodeFilter": "",
            "smartFilter": False,
            "previouslyMatchedEpisodes": [],
            "affectedFeeds": data.rss_link,
            "ignoreDays": 0,
            "lastMatch": "",
            "addPaused": False,
            "assignedCategory": "Bangumi",
            "savePath": data.save_path,
        }
        self.client.rss_set_rule(rule_name=data.rule_name, rule_def=rule)
        data.added = True
        logger.info(
            f"[Downloader] Add {data.official_title} Season {data.season} to auto download rules."
        )

    def set_rules(self, bangumi_info: list[Bangumi]):
        logger.debug("[Downloader] Start adding rules.")
        for info in bangumi_info:
            self.set_rule(info)
        logger.debug("[Downloader] Finished.")

    def get_torrent_info(self, category="Bangumi", status_filter="completed", tag=None):
        return self.client.torrents_info(
            status_filter=status_filter, category=category, tag=tag
        )

    def rename_torrent_file(self, _hash, old_path, new_path) -> bool:
        logger.info(f"{old_path} >> {new_path}")
        return self.client.torrents_rename_file(
            torrent_hash=_hash, old_path=old_path, new_path=new_path
        )

    def delete_torrent(self, hashes):
        self.client.torrents_delete(hashes)
        logger.info("[Downloader] Remove torrents.")

    def add_torrent(self, torrent: Torrent | list, bangumi: Bangumi) -> bool:
        if not bangumi.save_path:
            bangumi.save_path = self._gen_save_path(bangumi)
        with RequestContent() as req:
            if isinstance(torrent, list):
                if len(torrent) == 0:
                    logger.debug(
                        f"[Downloader] No torrent found: {bangumi.official_title}"
                    )
                    return False
                if "magnet" in torrent[0].url:
                    torrent_url = []
                    for t in torrent:
                        torrent_url.append(t.url)
                        t.hash = torrent_hash.from_magnet(t.url)
                    torrent_file = None
                else:
                    torrent_file = []
                    for t in torrent:
                        content = req.get_content(t.url)
                        torrent_file.append(content)
                        t.hash = torrent_hash.from_torrent(content)
                    torrent_url = None
                for t in torrent:
                    t.bangumi_id = bangumi.id
            else:
                if "magnet" in torrent.url:
                    torrent_url = torrent.url
                    torrent.hash = torrent_hash.from_magnet(torrent.url)
                    torrent_file = None
                else:
                    torrent_file = req.get_content(torrent.url)
                    torrent.hash = torrent_hash.from_torrent(torrent_file)
                    torrent_url = None
                torrent.bangumi_id = bangumi.id
        if self.client.add_torrents(
            torrent_urls=torrent_url,
            torrent_files=torrent_file,
            save_path=bangumi.save_path,
            category="Bangumi",
        ):
            logger.debug(f"[Downloader] Add torrent: {bangumi.official_title}")
            return True
        else:
            logger.debug(f"[Downloader] Torrent added before: {bangumi.official_title}")
            return False

    def move_torrent(self, hashes, location):
        self.client.move_torrent(hashes=hashes, new_location=location)

    # RSS Parts
    def add_rss_feed(self, rss_link, item_path="Mikan_RSS"):
        self.client.rss_add_feed(url=rss_link, item_path=item_path)

    def remove_rss_feed(self, item_path):
        self.client.rss_remove_item(item_path=item_path)

    def get_rss_feed(self):
        return self.client.rss_get_feeds()

    def get_download_rules(self):
        return self.client.get_download_rule()

    def get_torrent_path(self, hashes):
        return self.client.get_torrent_path(hashes)

    def set_category(self, hashes, category):
        self.client.set_category(hashes, category)

    def remove_rule(self, rule_name):
        self.client.remove_rule(rule_name)
        logger.info(f"[Downloader] Delete rule: {rule_name}")
