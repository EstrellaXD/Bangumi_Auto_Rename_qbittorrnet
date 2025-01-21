import logging

from module.models import Notification
from module.network import RequestContent
from module.utils.cache_image import str_to_url

logger = logging.getLogger(__name__)


class ServerChanNotification(RequestContent):
    """Server酱推送"""

    def __init__(self, token, **kwargs):
        super().__init__()
        self.notification_url = f"https://sctapi.ftqq.com/{token}.send"

    @staticmethod
    def gen_message(notify: Notification) -> str:
        if notify.episode:
            if notify.poster_path:
                notify.poster_path = str_to_url(notify.poster_path.split("/")[-1])
            notify.message += f"\n{notify.poster_path}\n".strip()

    async def post_msg(self, notify: Notification) -> bool:
        self.gen_message(notify)
        data = {
            "title": notify.title,
            "desp": notify.message,
        }
        async with RequestContent() as req:
            resp = await req.post_url(self.notification_url, data)
            logger.debug(f"ServerChan notification: {resp.status_code}")
            return resp.status_code == 200
