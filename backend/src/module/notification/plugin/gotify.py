import logging

from module.models import Notification
from module.network import RequestContent

logger = logging.getLogger(__name__)


class GotifyNotification(RequestContent):
    """gotify推送 无图"""

    def __init__(self, token, chat_id, **kwargs):
        super().__init__()
        # Chat_id is used as noti_url in this push tunnel
        self.notification_url = f"{chat_id}"
        self.token = token

    @staticmethod
    def gen_message(notify: Notification) -> str:
        text = f"""
        番剧名称：{notify.official_title}\n季度： 第{notify.season}季\n更新集数： 第{notify.episode}集\n{notify.poster_path}\n
        """
        return text.strip()

    def post_msg(self, notify: Notification) -> bool:
        ##Change message format to match Gotify push better
        title = "【番剧更新】" + notify.official_title
        message = self.gen_message(notify)
        data = {
            "title": title,
            "message": message,
        }
        if self.notification_url.find("?token=") != -1:
            post_url = self.notification_url
        else:
            post_url = f"{self.notification_url}?token={self.token}"
        resp = self.post_data(post_url, data)
        logger.debug(f"Gotify notification: {resp.status_code}")
        return resp.status_code == 200