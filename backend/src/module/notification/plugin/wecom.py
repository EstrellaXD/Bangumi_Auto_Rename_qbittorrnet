import logging

from module.models import Notification
from module.network import RequestContent
from module.utils.cache_image import str_to_url

logger = logging.getLogger(__name__)


class WecomNotification(RequestContent):
    """企业微信推送 基于图文消息"""

    def __init__(self, token, chat_id, **kwargs):
        super().__init__()
        # Chat_id is used as noti_url in this push tunnel
        self.notification_url = f"{chat_id}"
        self.token = token

    @staticmethod
    def gen_message(notify: Notification):

        if notify.episode:
            if notify.poster_path:
                notify.poster_path = str_to_url(notify.poster_path.split("/")[-1])
            notify.title = "【番剧更新】" + notify.title
            # Default pic to avoid blank in message. Resolution:1068*455
            if notify.poster_path == "https://mikanani.me":
                notify.poster_path = "https://article.biliimg.com/bfs/article/d8bcd0408bf32594fd82f27de7d2c685829d1b2e.png"
            notify.message += f"\n{notify.poster_path}\n".strip()

    async def post_msg(self, notify: Notification) -> bool:
        ##Change message format to match Wecom push better
        self.gen_message(notify)
        data = {
            "key": self.token,
            "type": "news",
            "title": notify.title,
            "msg": notify.message,
            "picurl": notify.poster_path,
        }
        async with RequestContent() as req:
            resp = req.post_url(self.notification_url, data)
            logger.debug(f"Wecom notification: {resp.status_code}")
            return resp.status_code == 200
