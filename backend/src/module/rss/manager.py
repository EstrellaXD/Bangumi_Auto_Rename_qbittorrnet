from module.database import Database, engine
from module.models import ResponseModel, RSSItem, Torrent
from module.models.rss import RSSUpdate
from module.network import RequestContent


class RSSManager():
    def __init__(self, _engine=engine):
        self.engine = _engine

    async def add_rss(
        self,
        rss_link: str,
        name: str | None = None,
        aggregate: bool = True,
        parser: str = "mikan",
    ):
        if not name:
            async with RequestContent() as req:
                name = await req.get_rss_title(rss_link)
                if not name:
                    return False

        rss_data = RSSItem(name=name, url=rss_link, aggregate=aggregate, parser=parser)

        with Database(self.engine) as db:
            db.rss.add(rss_data)
            return True

        # return ResponseModel(
        #     status=False,
        #     status_code=406,
        #     msg_en="RSS added failed.",
        #     msg_zh="RSS 添加失败。",
        # )

    def disable_list(self, rss_id_list: list[int]):
        with Database(self.engine) as db:
            for rss_id in rss_id_list:
                db.rss.disable(rss_id)
        return True

    def enable_list(self, rss_id_list: list[int]):
        with Database(self.engine) as db:
            for rss_id in rss_id_list:
                db.rss.enable(rss_id)

    def delete_list(self, rss_id_list: list[int]):

        with Database(self.engine) as db:
            for rss_id in rss_id_list:
                db.rss.delete(rss_id)
        return ResponseModel(
            status=True,
            status_code=200,
            msg_en="Delete RSS successfully.",
            msg_zh="删除 RSS 成功。",
        )

    def delete(self,rss_id:int):
        with Database(self.engine) as db:
            return db.rss.delete(rss_id)

    def disable(self,rss_id:int):
        with Database(self.engine) as db:
            return db.rss.disable(rss_id)


    def update(self,rss_id:int,data:RSSUpdate):
        with Database(self.engine) as manager:
            return manager.rss.update(rss_id, data)

    def search_all(self):
        with Database(self.engine) as db:
            return db.rss.search_all()

    def get_rss_torrents(self, rss_id: int) -> list[Torrent]:
        with Database(self.engine) as db:
            rss = db.rss.search_id(rss_id)
            if rss:
                return db.torrent.search_rss(rss_id)
            else:
                return []

if __name__ == "__main__":
    import asyncio
    test = RSSManager(engine)
    rss_link = "https://mikanani.me/RSS/Bangumi?bangumiId=3407&subgroupid=583"
    ans = asyncio.run(test.add_rss(rss_link))
    ans = test.disable_list([1])

