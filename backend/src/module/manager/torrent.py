import logging

from module.database import Database
from module.downloader import DownloadClient
from module.models import Bangumi, BangumiUpdate, ResponseModel
from module.parser import TitleParser

logger = logging.getLogger(__name__)


class TorrentManager(Database):
    @staticmethod
    def __match_torrents_list(data: Bangumi | BangumiUpdate) -> list:
        with DownloadClient() as client:
            torrents = client.get_torrent_info(status_filter=None)
        return [
            torrent.hash for torrent in torrents if torrent.save_path == data.save_path
        ]

    def delete_torrents(self, data: Bangumi, client: DownloadClient):
        hash_list = self.__match_torrents_list(data)
        if hash_list:
            client.delete_torrent(hash_list)
            logger.info(f"Delete rule and torrents for {data.official_title}")
            return ResponseModel(
                status_code=200,
                status=True,
                msg_en=f"Delete rule and torrents for {data.official_title}",
                msg_zh=f"删除 {data.official_title} 规则和种子",
            )
        else:
            return ResponseModel(
                status_code=406,
                status=False,
                msg_en=f"Can't find torrents for {data.official_title}",
                msg_zh=f"无法找到 {data.official_title} 的种子",
            )

    def delete_rule(self, _id: int | str, file: bool = False):
        data = self.bangumi.search_id(int(_id))
        if isinstance(data, Bangumi):
            with DownloadClient() as client:
                self.rss.delete(data.official_title)
                self.bangumi.delete_one(int(_id))
                self.torrent.delete_by_bangumi_id(int(_id))
                if file:
                    torrent_message = self.delete_torrents(data, client)
                logger.info(f"[Manager] Delete rule for {data.official_title}")
                return ResponseModel(
                    status_code=200,
                    status=True,
                    msg_en=f"Delete rule for {data.official_title}. {torrent_message.msg_en if file else ''}",
                    msg_zh=f"删除 {data.official_title} 规则。{torrent_message.msg_zh if file else ''}",
                )
        else:
            return ResponseModel(
                status_code=406,
                status=False,
                msg_en=f"Can't find id {_id}",
                msg_zh=f"无法找到 id {_id}",
            )

    def disable_rule(self, _id: str | int, file: bool = False):
        data = self.bangumi.search_id(int(_id))
        if isinstance(data, Bangumi):
            with DownloadClient() as client:
                # client.remove_rule(data.rule_name)
                data.deleted = True
                self.bangumi.update(data)
                if file:
                    torrent_message = self.delete_torrents(data, client)
                    return torrent_message
                logger.info(f"[Manager] Disable rule for {data.official_title}")
                return ResponseModel(
                    status_code=200,
                    status=True,
                    msg_en=f"Disable rule for {data.official_title}",
                    msg_zh=f"禁用 {data.official_title} 规则",
                )
        else:
            return ResponseModel(
                status_code=406,
                status=False,
                msg_en=f"Can't find id {_id}",
                msg_zh=f"无法找到 id {_id}",
            )

    def enable_rule(self, _id: str | int):
        data = self.bangumi.search_id(int(_id))
        if data:
            data.deleted = False
            self.bangumi.update(data)
            logger.info(f"[Manager] Enable rule for {data.official_title}")
            return ResponseModel(
                status_code=200,
                status=True,
                msg_en=f"Enable rule for {data.official_title}",
                msg_zh=f"启用 {data.official_title} 规则",
            )
        else:
            return ResponseModel(
                status_code=406,
                status=False,
                msg_en=f"Can't find id {_id}",
                msg_zh=f"无法找到 id {_id}",
            )

    def update_rule(self, bangumi_id, data: BangumiUpdate):
        old_data: Bangumi = self.bangumi.search_id(bangumi_id)
        if old_data:
            # Move torrent
            match_list = self.__match_torrents_list(old_data)
            with DownloadClient() as client:
                path = client._gen_save_path(data)
                if match_list:
                    client.move_torrent(match_list, path)
            data.save_path = path
            self.bangumi.update(data, bangumi_id)
            return ResponseModel(
                status_code=200,
                status=True,
                msg_en=f"Update rule for {data.official_title}",
                msg_zh=f"更新 {data.official_title} 规则",
            )
        else:
            logger.error(f"[Manager] Can't find data with {bangumi_id}")
            return ResponseModel(
                status_code=406,
                status=False,
                msg_en=f"Can't find data with {bangumi_id}",
                msg_zh=f"无法找到 id {bangumi_id} 的数据",
            )

    def refresh_poster(self):
        bangumis = self.bangumi.search_all()
        for bangumi in bangumis:
            if not bangumi.poster_link:
                TitleParser().tmdb_poster_parser(bangumi)
        self.bangumi.update_all(bangumis)
        return ResponseModel(
            status_code=200,
            status=True,
            msg_en="Refresh poster link successfully.",
            msg_zh="刷新海报链接成功。",
        )

    def refind_poster(self, bangumi_id: int):
        bangumi = self.bangumi.search_id(bangumi_id)
        TitleParser().tmdb_poster_parser(bangumi)
        self.bangumi.update(bangumi)
        return ResponseModel(
            status_code=200,
            status=True,
            msg_en="Refresh poster link successfully.",
            msg_zh="刷新海报链接成功。",
        )

    def search_all_bangumi(self):
        datas = self.bangumi.search_all()
        if not datas:
            return []
        return [data for data in datas if not data.deleted]

    def search_one(self, _id: int | str):
        data = self.bangumi.search_id(int(_id))
        if not data:
            logger.error(f"[Manager] Can't find data with {_id}")
            return ResponseModel(
                status_code=406,
                status=False,
                msg_en=f"Can't find data with {_id}",
                msg_zh=f"无法找到 id {_id} 的数据",
            )
        else:
            return data


if __name__ == "__main__":
    with TorrentManager() as manager:
        manager.refresh_poster()
