import logging

from module.conf import POSTERS_PATH
from module.database import Database

logger = logging.getLogger(__name__)


def start_up():
    with Database() as engine:
        engine.create_table()
        engine.user.add_default_user()


def first_run():
    with Database() as engine:
        engine.create_table()
        engine.user.add_default_user()
    POSTERS_PATH.mkdir(parents=True, exist_ok=True)
