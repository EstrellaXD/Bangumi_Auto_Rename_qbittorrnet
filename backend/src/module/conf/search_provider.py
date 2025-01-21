from pathlib import Path

from module.utils import json_config

DEFAULT_PROVIDER = {
    "mikan": "https://mikanani.me/RSS/Search?searchstr=%s",
    "nyaa": "https://nyaa.si/?page=rss&q=%s&c=0_0&f=0",
    "dmhy": "http://dmhy.org/topics/rss/rss.xml?keyword=%s",
}

PROVIDER_PATH = Path("config/search_provider.json")


def load_provider():
    if PROVIDER_PATH.exists():
        return json_config.load(PROVIDER_PATH)
    else:
        json_config.save(PROVIDER_PATH, DEFAULT_PROVIDER)
        return DEFAULT_PROVIDER


SEARCH_CONFIG: dict[str, str] = load_provider()
