from module.conf import LEGACY_DATA_PATH
from module.database import Database
from module.models import Bangumi
from module.rss.manager import RSSManager
from module.utils import json_config


async def data_migration():
    if not LEGACY_DATA_PATH.exists():
        return False
    old_data = json_config.load(LEGACY_DATA_PATH)
    infos = old_data["bangumi_info"]
    rss_link = old_data["rss_link"]
    new_data = []
    for info in infos:
        new_data.append(Bangumi(**info, rss_link=rss_link))
    with Database() as engine:
        engine.bangumi.add_all(new_data)
    engine = RSSManager()
    await engine.add_rss(rss_link)
    LEGACY_DATA_PATH.unlink(missing_ok=True)


def database_migration():
    with Database() as engine:
        engine.migrate()
