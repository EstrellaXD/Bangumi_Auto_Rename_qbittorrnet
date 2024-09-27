from module.models import Notification
from module.notification import PostNotification


class TestPostNotification(PostNotification):
    @staticmethod
    def _get_poster(notify: Notification):
        notify.poster_path = notify.poster_path


def test_notification():
    info1 = Notification(
        official_title="番剧名",
        season=1,
        episode=1,
        poster_path="https://mikanime.tv/images/Bangumi/202404/0fd46fc8.jpg",
    )
    info2 = Notification(
        official_title="番剧名",
        season=1,
        episode=1,
        poster_path="posters/0fd46fc8.jpg",
    )
    with TestPostNotification() as notifier:
        assert notifier.send_msg(info1)
        assert notifier.send_msg(info2)
