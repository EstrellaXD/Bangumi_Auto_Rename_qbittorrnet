import asyncio
import base64
import hashlib
import logging
from urllib.parse import quote

import bencodepy

from module.downloader.client import Downloader
from module.models import Bangumi, Torrent
from module.network import RequestContent
from module.utils import get_hash

from .path import TorrentPath

logger = logging.getLogger(__name__)


class DownloadClient():
    # 对下载器的封装,提供下载器的基本操作,将一些封装为对象
    # 检查下载器是否可用,下载器的基本操作,下载器的基本信息
    #
    def __init__(self):
        super().__init__()
        self._path_parser = TorrentPath()
        self._client = Downloader()


    async def __aenter__(self):
        await self._client.auth()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._client.close()

    async def get_torrent_info(
        self, category="Bangumi", status_filter="completed", tag=None, limit=0
    ):
        resp = await self.torrents_info(
            status_filter=status_filter, category=category, tag=tag, limit=limit
        )
        return resp
    async def rename_torrent_file(self, _hash, old_path, new_path) -> bool:
        resp = await self.rename(
            torrent_hash=_hash, old_path=old_path, new_path=new_path
        )
        logger.info(f"[Downloader] rename {old_path} >> {new_path}")
        return resp
    async def delete_torrent(self, hashes):
        resp = await self.delete(hashes)
        logger.info(f"[Downloader] Remove torrents {hashes}.")
        return resp

    async def add_torrent(self, torrent: Torrent, bangumi) -> bool:
        bangumi.save_path = self._path_parser.gen_save_path(bangumi)
        torrent_file = None
        torrent_url = torrent.url
        # print(f"add torrent {torrent.url}")
        if "magnet" in torrent.url:
            torrent_url = torrent.url
        else:
            async with RequestContent() as req:
                # 下载种子文件,处理 hash 与 url 不一致的情况
                if torrent_file := await req.get_content(torrent.url):
                    torrent_url_hash = get_hash(torrent_url)
                    torrent_url = await self.torrent_to_link(torrent_file)
                    torrent_hash = get_hash(torrent_url)
                    if torrent_hash != torrent_url_hash:
                        torrent.url = f"{torrent.url},{torrent_hash}"
        logging.debug(f"[Downloader] send url {torrent_url}to downloader ")

        result = await self.add(
            torrent_urls=torrent_url,
            torrent_files=torrent_file,
            save_path=bangumi.save_path,
            category="Bangumi",
        )
        if result:
            logger.debug(f"[Downloader] Add torrent: {torrent.name}")
            return True
        else:
            logger.warning(
                f"[Downloader] Torrent added failed: {torrent.name},{torrent.url=}"
            )
        return False

    async def add_torrents(
        self, torrents: list[Torrent] | Torrent, bangumi: Bangumi
    ) -> list[bool | BaseException]:
        tasks = []
        if isinstance(torrents, Torrent):
            torrents = [torrents]
        for torrent in torrents:
            tasks.append(self.add_torrent(torrent, bangumi))

        result = await asyncio.gather(*tasks, return_exceptions=True)
        return result

    async def move_torrent(self, hashes, location):
        await self.move(hashes=hashes, new_location=location)

    async def set_category(self, hashes, category):
        await self.set_category(hashes, category)

    async def torrent_to_link(self, torrent_file):
        torrent_info = bencodepy.decode(torrent_file)

        # 获取 info 字段并进行 bencode 编码
        info = torrent_info[b"info"]
        encoded_info = bencodepy.encode(info)

        # 计算 info_hash (SHA1 hash of the encoded info dictionary)
        info_hash = hashlib.sha1(encoded_info).digest()

        # 将 hash 转换为磁力链接格式
        info_hash_hex = base64.b16encode(info_hash).decode("utf-8").lower()

        # 获取文件名
        name = torrent_info.get(b"info", {}).get(b"name", b"").decode("utf-8")

        # 构建磁力链接
        magnet_link = f"magnet:?xt=urn:btih:{info_hash_hex}"
        if name:
            magnet_link += f"&dn={quote(name)}"

        # 添加 trackers (可选)
        if b"announce" in torrent_info:
            tracker = torrent_info[b"announce"].decode("utf-8")
            magnet_link += f"&tr={quote(tracker)}"

        if b"announce-list" in torrent_info:
            for tracker_list in torrent_info[b"announce-list"]:
                tracker = tracker_list[0].decode("utf-8")
                magnet_link += f"&tr={quote(tracker)}"
        return magnet_link
