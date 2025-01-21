import asyncio
import logging

from module.conf import settings
from module.database import Database
from module.models import Notification
from module.notification.plugin import Notification as Notifier

logger = logging.getLogger(__name__)


class PostNotification:
    """
    对通知进行处理, 调用 setting 的 notification
    """

    def __init__(self) -> None:
        chat_ids = settings.notification.chat_id.split(",")
        # 支持 多通知帐户
        self.notifier = [
            Notifier(
                token=settings.notification.token,
                chat_id=chat_id,
            )
            for chat_id in chat_ids
        ]

    def parse(self, notify: Notification):
        if notify.episode:
            if not notify.poster_path:
                self._get_poster(notify)
            if isinstance(notify.episode, float) and notify.episode.is_integer():
                notify.episode = int(notify.episode)
            notify.message = f"""
            番剧名称：{notify.title}\n季度： 第{notify.season}季\n更新集数： 第{notify.episode}集
            """.strip()

    @staticmethod
    def _get_poster(notify: Notification):
        """
        有可能传过来的是没有海报的番剧
        比如 collection 的番剧
        获取番剧海报
        """
        with Database() as db:
            poster_path = db.bangumi.match_poster(notify.title)
        notify.poster_path = poster_path

    async def send(self, notify: Notification):
        self.parse(notify)
        try:
            for notifier in self.notifier:
                await notifier.post_msg(notify)
            logger.debug(f"Send notification: {notify.title}")
        except Exception as e:
            logger.warning(f"Failed to send notification: {e}")
            return False


if __name__ == "__main__":
    import asyncio

    title = "败犬"
    # link = "posters/aHR0cHM6Ly9pbWFnZS50bWRiLm9yZy90L3Avdzc4MC9wYWRSbWJrMkxkTGd1ZGg1Y0xZMG85VEZ6aEkuanBn"
    nt = Notification(title=title, season=1, episode=2, poster_path=None)
    asyncio.run(PostNotification().send(nt))
