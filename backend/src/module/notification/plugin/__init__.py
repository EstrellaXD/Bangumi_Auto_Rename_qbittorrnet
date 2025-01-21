# from module.conf import settings

# from .bark import BarkNotification
# from .log_notification import LogNotification
# from .server_chan import ServerChanNotification
# from .telegram import TelegramNotification
# from .wecom import WecomNotification

import importlib
import logging

from module.conf import settings
from module.notification.plugin.base_notification import BaseNotification

logger = logging.getLogger(__name__)

if settings.notification.enable:
    notification_type = settings.notification.type
    package_path = f"module.notification.plugin.{notification_type}"
else:
    package_path = "module.notification.plugin.log_notification"

notification: BaseNotification = importlib.import_module(package_path)
Notification = notification.Notification


# def getClient(type: str):
#     notifiers = {
#         "telegram": TelegramNotification,
#         "server-chan": ServerChanNotification,
#         "bark": BarkNotification,
#         "wecom": WecomNotification,
#     }
#     return notifiers.get(type.lower(), LogNotification)
#
#
# Notifier = getClient(settings.notification.type)


__all__ = [
    "BarkNotification",
    "ServerChanNotification",
    "TelegramNotification",
    "WecomNotification",
]
