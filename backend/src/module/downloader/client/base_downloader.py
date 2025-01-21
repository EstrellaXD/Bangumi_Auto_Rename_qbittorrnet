from abc import ABCMeta, abstractmethod


# 主要实现以下 个功能
# 1. renamer,用以实现重命名功能 hash, old name, new name
# 2. move, 用以实现改数据后的转移
# 3. add, 用以加种子
# 4. get_info, 获取当前所有的有关种子
# 5. auth, 用以登陆
# 6. check_host, 用以检查连通性
# 7. logout,用以登出
#
class BaseDownloader(metaclass=ABCMeta):
    @abstractmethod
    async def auth(self):
        pass

    @abstractmethod
    async def check_host(self):
        pass

    @abstractmethod
    async def logout(self):
        pass

    @abstractmethod
    async def get_torrent_files(self, hash):
        pass
    @abstractmethod
    async def torrents_info(self, status_filter , category , tag, limit):
        pass

    @abstractmethod
    async def rename(self, torrent_hash,old_path, new_path):
        pass
    @abstractmethod
    async def move(self, hashes, new_location):
        pass
    @abstractmethod
    async def add(self, torrent_urls, torrent_files, save_path, category):
        pass
    @abstractmethod
    async def delete(self, hashes):
        pass


