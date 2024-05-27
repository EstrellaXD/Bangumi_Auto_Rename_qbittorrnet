import logging

from module.conf import LEGACY_DATA_PATH
from module.models import Bangumi, Torrent
from module.rss import RSSEngine
from module.utils import json_config, torrent_hash
from module.network import RequestContent

logger = logging.getLogger(__name__)


def data_migration():
    if not LEGACY_DATA_PATH.exists():
        return False
    old_data = json_config.load(LEGACY_DATA_PATH)
    infos = old_data["bangumi_info"]
    rss_link = old_data["rss_link"]
    new_data = []
    for info in infos:
        new_data.append(Bangumi(**info, rss_link=rss_link))
    with RSSEngine() as engine:
        engine.bangumi.add_all(new_data)
        engine.add_rss(rss_link)
    LEGACY_DATA_PATH.unlink(missing_ok=True)


def database_migration():
    with RSSEngine() as engine:
        engine.migrate()


def torrent_migration():
    with RSSEngine() as db, RequestContent() as req:
        engine = db.engine
        torrents = db.exec("SELECT * FROM torrent").all()
        torrents = [dict(torrent) for torrent in torrents]
        for torrent in torrents:
            torrent["refer_id"] = torrent["bangumi_id"]
            if torrent.get("hash") or torrent.get("bangumi_id") is None:
                continue
            logger.debug(f"Get {torrent['name']} Hash")
            url = torrent["url"]
            if url.startswith("magnet"):
                info_hash = torrent_hash.from_magnet(url)
            else:
                content = req.get_content(url)
                info_hash = torrent_hash.from_torrent(content)
            torrent["hash"] = info_hash
        readd_torrents = [Torrent(**torrent) for torrent in torrents]
        Torrent.__table__.drop(engine)
        Torrent.__table__.create(engine)
        db.commit()
        db.torrent.add_all(readd_torrents)
        db.commit()
