import logging

import requests

from module.models import Notification
from module.network import RequestContent

logger = logging.getLogger(__name__)


class WecomRobotNotification(RequestContent):
    """企业微信群机器人"""

    def __init__(self, token, chat_id, **kwargs):
        super().__init__()
        # token is wecom group robot webhook key
        self.notification_url = (
            f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={token}"
        )

    @staticmethod
    def gen_message(notify: Notification) -> str:
        text = f"""
        番剧名称：{notify.official_title}\n季度： 第{notify.season}季\n更新集数： 第{notify.episode}集
        """
        return text.strip()

    def post_msg(self, notify: Notification) -> bool:
        title = "【番剧更新】"
        msg = self.gen_message(notify)
        picurl = notify.poster_path
        if picurl.startswith("http"):
            data = {
                "msgtype": "news",
                "news": {
                    "articles": [
                        {
                            "title": title,
                            "description": msg,
                            "url": "https://mikanime.tv",
                            "picurl": picurl,
                        }
                    ]
                },
            }
        else:
            msg = f"{title}\n{msg}"
            data = {"msgtype": "text", "text": {"content": msg}}
        resp = requests.post(url=self.notification_url, json=data, timeout=3)
        logger.debug(f"Wecom-robot notification: {resp.status_code}")
        return resp.status_code == 200
