import logging

from module.models import Notification
from module.notification.plugin.base_notification import BaseNotification

logger = logging.getLogger(__name__)


class LogNotification(BaseNotification):

    def __init__(self, token, **kwargs):
        super().__init__()

    async def post_msg(self, notify: Notification) -> bool:
        logger.info(f"[Notification] {notify.message}")
        return True
