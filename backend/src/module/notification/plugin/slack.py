import logging

from module.models import Notification
from module.network import RequestContent
from module.utils.cache_image import str_to_url

logger = logging.getLogger(__name__)


class SlackNotification(RequestContent):
    def __init__(self, token, **kwargs):
        super().__init__()
        self.token = token
        self.notification_url = "https://api.day.app/push"

    @staticmethod
    def gen_message(notify: Notification):
        if notify.episode:
            if notify.poster_path:
                notify.poster_path = str_to_url(notify.poster_path.split("/")[-1])


    async def post_msg(self, notify: Notification) -> bool:
        self.gen_message(notify)
        data = {"title": notify.title, "body": notify.message, "device_key": self.token}
        async with RequestContent() as req:
            resp = await req.post_url(self.notification_url, data)
            logger.debug(f"Bark notification: {resp.status_code}")
            return resp.status_code == 200
