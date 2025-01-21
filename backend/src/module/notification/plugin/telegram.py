import logging

from module.models import Notification
from module.network import RequestContent
from module.notification.plugin.base_notification import BaseNotification
from module.utils import load_image

logger = logging.getLogger(__name__)


class Notification(BaseNotification):
    def __init__(self, token, chat_id):
        self.photo_url = f"https://api.telegram.org/bot{token}/sendPhoto"
        self.message_url = f"https://api.telegram.org/bot{token}/sendMessage"
        self.chat_id = chat_id

    def gen_message(self, notify: Notification):
        # notify.message+="\nhello"
        pass

    async def post_msg(self, notify: Notification) -> bool:
        self.gen_message(notify)
        data = {
            "chat_id": self.chat_id,
            "caption": notify.message,
            "text": notify.message,
            "disable_notification": True,
        }
        photo = None
        if notify.poster_path:
            photo = await load_image(notify.poster_path)

        if photo:
            async with RequestContent() as req:
                resp = await req.post_url(self.photo_url, data, files={"photo": photo})
        else:
            async with RequestContent() as req:
                resp = await req.post_url(self.message_url, data)
            # resp = await self.post_data(self.message_url, data)
        logger.debug(f"Telegram notification: {resp.status_code}")
        return resp and resp.status_code == 200
