import logging
from logging import NullHandler
from pathlib import Path

from .config import settings

LOG_ROOT = Path("data")
LOG_PATH = LOG_ROOT / "log.txt"


def setup_logger(level: int = logging.INFO, reset: bool = False):
    level = logging.DEBUG if settings.log.debug_enable else level
    LOG_ROOT.mkdir(exist_ok=True)
    if reset and LOG_PATH.exists():
        LOG_PATH.unlink(missing_ok=True)

    logging.addLevelName(logging.DEBUG, "DEBUG:")
    logging.addLevelName(logging.INFO, "INFO:")
    logging.addLevelName(logging.WARNING, "WARNING:")
    LOGGING_FORMAT = "[%(asctime)s] %(levelname)-8s %(message)s"
    TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    logging.basicConfig(
        level=level,
        format=LOGGING_FORMAT,
        datefmt=TIME_FORMAT,
        encoding="utf-8",
        handlers=[
            logging.FileHandler(LOG_PATH, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )
    loggers_to_silence = [
        "httpx",
        "httpcore",
        "hpack",
        "hpack.hpack",
    ]
    for logger_name in loggers_to_silence:
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.WARNING)
        # logger.propagate = False
        # logger.handlers = [NullHandler()]

    # 完全抑制 httpx 的日志输出
    # httpx_logger = logging.getLogger("httpx")
    # http_coro_logger = logging.getLogger("httpcore")
    # httpx_logger.setLevel(logging.WARNING)
    # http_coro_logger.setLevel(logging.WARNING)
    # httpx_logger.addHandler(NullHandler())
    # http_coro_logger.addHandler(NullHandler())
    # httpx_logger.propagate = False
    # http_coro_logger.propagate = False
