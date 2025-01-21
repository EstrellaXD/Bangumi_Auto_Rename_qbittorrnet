from abc import abstractmethod

from module.models import Notification


class BaseNotification:

    @abstractmethod
    def __init__(self, token, **kwargs):
        pass


    @abstractmethod
    async def post_msg(self, notify: Notification) -> bool:
        pass
