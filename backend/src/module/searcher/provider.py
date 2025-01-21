import re

from module.conf import SEARCH_CONFIG
from module.models import RSSItem


def search_url(site: str, keywords: list[str]) -> RSSItem:
    """
    根据关键词和站点搜索 RSS 链接
    如果是 mikan , 那么 rss 的 parser 会设置为 mikan
    如果是 其他 , 那么 rss 的 parser 会设置为 tmdb
    """
    keyword = "+".join(keywords)
    search_str = re.sub(r"[\W_ ]", "+", keyword)
    if site in SEARCH_CONFIG.keys():
        url = re.sub(r"%s", search_str, SEARCH_CONFIG[site])
        parser = "mikan" if site == "mikan" else "tmdb"
        rss_item = RSSItem(
            url=url,
            aggregate=False,
            parser=parser,
        )
        return rss_item
    else:
        raise ValueError(f"Site {site} is not supported")
