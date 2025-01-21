import asyncio
import base64
import hashlib
import importlib
import logging
from asyncio import Task
from typing import Any, Callable
from urllib.parse import quote

import bencodepy

from module.models import Bangumi, Torrent
from module.network import RequestContent
from module.utils import get_hash

from ..conf import settings
from .client import AuthorizationError, BaseDownloader
from .path import TorrentPath

logger = logging.getLogger(__name__)


class DownloadClient:
    """ """

    # 自动获取下载器
    # 下载器登陆错误时自动重试
    def __init__(self):
        self.downloader: BaseDownloader = self.get_downloader()
        self._path_parser: TorrentPath = TorrentPath()
        self.tasks: list[Task[Any]] = []
        self.login_lock: asyncio.Lock = asyncio.Lock()
        self.is_logining: bool = False
        self.is_running: bool = True
        # 用于等待登陆完成
        self.login_event: asyncio.Event = asyncio.Event()
        self.login_success_event: asyncio.Event = asyncio.Event()


    async def __aenter__(self):
        self.start()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def login(self):
        # 当没有登陆,并且没有登陆事件时
        try:
            self.is_logining = True
            while True:
                await self.login_event.wait()
                self.login_success_event.clear()
                if await self.downloader.auth():
                    # self.is_login = True
                    self.login_success_event.set()
                    self.login_event.clear()
                else:
                    logger.info("[Downloader] login failed, retry after 30s")
                    await asyncio.sleep(30)
        except Exception as e:
            logger.error(f"[Downloader] login error {e}")
            self.is_logining = False

    async def _get_torrent_info(
        self, category: str, status_filter: str, tag: str, limit: int
    ):

        resp = await self.downloader.torrents_info(
            status_filter=status_filter, category=category, tag=tag, limit=limit
        )
        return resp

    async def get_torrent_info(
        self, category="Bangumi", status_filter="completed", tag=None, limit=0
    ):
        return await self._add_wrapper(
            self._get_torrent_info, category, status_filter, tag, limit
        )

    async def _add_torrent(self, torrent: Torrent, bangumi) -> bool:
        bangumi.save_path = self._path_parser.gen_save_path(bangumi)
        torrent_file = None
        torrent_url = torrent.url
        # print(f"add torrent {torrent.url}")
        if torrent.url.startswith("magnet"):
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

        result = await self.downloader.add(
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

    async def add_torrent(self, torrent: Torrent, bangumi: Bangumi) -> bool:
        return await self._add_wrapper(self._add_torrent, torrent, bangumi)

    async def _move_torrent(self, hashes, location):
        await self.downloader.move(hashes=hashes, new_location=location)

    async def move_torrent(self, hashes, location):
        return await self._add_wrapper(self._move_torrent, hashes, location)

    # async def set_category(self, hashes, category):
    #     await self.downloader.set_category(hashes, category)

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

    async def _rename_torrent_file(self, torrent_hash, old_path, new_path) -> bool:
        resp = await self.downloader.rename(
            torrent_hash=torrent_hash, old_path=old_path, new_path=new_path
        )
        logger.info(f"[Downloader] rename {old_path} >> {new_path}")
        return resp

    async def rename_torrent_file(self, torrent_hash, old_path, new_path) -> bool:
        return await self._add_wrapper(
            self._rename_torrent_file, torrent_hash, old_path, new_path
        )

    async def _delete_torrent(self, hashes):
        resp = await self.downloader.delete(hashes)
        logger.info(f"[Downloader] Remove torrents {hashes}.")
        return resp

    async def delete_torrent(self, hashes):
        return await self._add_wrapper(self._delete_torrent, hashes)

    async def _get_torrent_files(self, _hash: str) -> list[str]:
        return await self.downloader.get_torrent_files(_hash)

    async def get_torrent_files(self, _hash: str) -> list[str]:
        return await self._add_wrapper(self._get_torrent_files, _hash)

    def start(self):
        self.is_running = True
        self.downloader = self.get_downloader()
        # 判断有没有 login task
        if not self.is_logining:
            self.login_event.set()
            asyncio.create_task(self.login(), name="login")

    def stop(self):
        self.is_running = False
        for task in self.tasks:
            task.cancel()

    def restart(self):
        self.stop()
        self.start()

    async def _add_wrapper(self, operation: Callable, *args, **kwargs):
        # 等待登陆完成
        await self.login_success_event.wait()
        try:
            # 不加入重复任务
            for task in self.tasks:
                if task.get_name() == f"{operation.__name__}_{args}_{kwargs}":
                    return False
            task = asyncio.create_task(
                operation(*args, **kwargs), name=f"{operation.__name__}_{args}_{kwargs}"
            )
            self.tasks.append(task)
            res = await task
            self.tasks.remove(task)
            return res
        except AuthorizationError:
            # 取消现在所有task
            for task in self.tasks:
                task.cancel()
            self.tasks.clear()
            self.login_event.set()
            await self.downloader.auth()
            # 重新执行所有task
            for task in self.tasks:
                await task
        # 捕捉取消异常
        except asyncio.CancelledError:
            # 防止无法取消
            if not self.is_running:
                return
            # 重新添加task
            res = await self._add_wrapper(operation, *args, **kwargs)
            return res

    def get_downloader(self) -> BaseDownloader:
        download_type = settings.downloader.type
        package_path = f".client.{download_type}"
        downloader = importlib.import_module(package_path, package=__package__)
        # __package__ is the name of the package of the current module
        return downloader.Downloader()

Client = DownloadClient()
