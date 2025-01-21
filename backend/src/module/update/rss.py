from module.rss import RSSManager


async def update_main_rss(rss_link: str):
    engine = RSSManager()
    await engine.add_rss(rss_link, "main", True)
