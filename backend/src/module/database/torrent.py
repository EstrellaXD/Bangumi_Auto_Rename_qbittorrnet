import logging
from typing import Optional

from sqlmodel import Session, select, and_, desc

from module.models import Torrent

logger = logging.getLogger(__name__)


class TorrentDatabase:
    def __init__(self, session: Session):
        self.session = session

    def add(self, data: Torrent):
        self.session.add(data)
        self.session.commit()
        self.session.refresh(data)
        logger.debug(f"Insert {data.name} in database.")

    def add_all(self, datas: list[Torrent]):
        self.session.add_all(datas)
        self.session.commit()
        logger.debug(f"Insert {len(datas)} torrents in database.")

    def update(self, data: Torrent):
        self.session.add(data)
        self.session.commit()
        self.session.refresh(data)
        logger.debug(f"Update {data.name} in database.")

    def update_all(self, datas: list[Torrent]):
        self.session.add_all(datas)
        self.session.commit()

    def update_one_user(self, data: Torrent):
        self.session.add(data)
        self.session.commit()
        self.session.refresh(data)
        logger.debug(f"Update {data.name} in database.")

    def search(self, _id: int) -> Torrent:
        return self.session.exec(select(Torrent).where(Torrent.id == _id)).first()

    def search_all(self) -> list[Torrent]:
        return self.session.exec(select(Torrent)).all()

    def search_rss(self, rss_id: int) -> list[Torrent]:
        return self.session.exec(select(Torrent).where(Torrent.rss_id == rss_id)).all()

    def check_new(self, torrents_list: list[Torrent]) -> list[Torrent]:
        new_torrents = []
        old_torrents = self.search_all()
        old_urls = [t.url for t in old_torrents]
        for torrent in torrents_list:
            if torrent.url not in old_urls:
                new_torrents.append(torrent)
        return new_torrents

    def get_bangumi_id(self, torrent_hash: str) -> Optional[int]:
        return self.session.exec(
            select(Torrent.bangumi_id)
            .where(and_(Torrent.hash == torrent_hash, Torrent.bangumi_id.isnot(None)))
            .order_by(desc(Torrent.id))
        ).first()

    def delete_by_bangumi_id(self, bangumi_id: int):
        statement = select(Torrent).where(Torrent.bangumi_id == bangumi_id)
        torrents = self.session.exec(statement).all()
        for torrent in torrents:
            logger.debug(f"[Database] Delete torrent name: {torrent.name}.")
            self.session.delete(torrent)
        self.session.commit()
