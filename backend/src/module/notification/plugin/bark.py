import logging

from module.models import Notification
from module.network import RequestContent

logger = logging.getLogger(__name__)


class BarkNotification(RequestContent):
    def __init__(self, token, **kwargs):
        super().__init__()
        self.token = token
        self.notification_url = "https://api.day.app/push"

    @staticmethod
    def gen_message(notify: Notification) -> str:
        text = f"""
        番剧名称：{notify.title}\n季度： 第{notify.season}季\n更新集数： 第{notify.episode}集\n{notify.poster_path}\n
        """
        return text.strip()

    async def post_msg(self, notify: Notification) -> bool:
        text = self.gen_message(notify)
        data = {
            "title": notify.title,
            "body": text,
            "icon": notify.poster_path,
            "device_key": self.token,
        }
        resp = self.post_data(self.notification_url, data)
        logger.debug(f"Bark notification: {resp.status_code}")
        return resp.status_code == 200
