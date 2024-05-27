import asyncio
import threading

from module.checker import Checker
from module.conf import LEGACY_DATA_PATH


class ProgramStatus(Checker):
    def __init__(self):
        super().__init__()
        self.stop_event = threading.Event()
        self.lock = threading.Lock()
        self._downloader_status = False
        self._torrents_status = False
        self.event = asyncio.Event()

    @property
    def is_running(self):
        if self.stop_event.is_set() or self.check_first_run():
            return False
        else:
            return True

    @property
    def is_stopped(self):
        return self.stop_event.is_set()

    @property
    def downloader_status(self):
        if not self._downloader_status:
            self._downloader_status = self.check_downloader()
        return self._downloader_status

    @property
    def enable_rss(self):
        return self.check_analyser()

    @property
    def enable_renamer(self):
        return self.check_renamer()

    @property
    def first_run(self):
        return self.check_first_run()

    @property
    def legacy_data(self):
        return LEGACY_DATA_PATH.exists()

    @property
    def version_update(self):
        return not self.check_version()

    @property
    def database(self):
        return self.check_database()

    @property
    def img_cache(self):
        return self.check_img_cache()

    @property
    def torrent_hash(self):
        return self.check_torrent_hash()
