import re
from abc import ABC, abstractmethod

from bs4 import BeautifulSoup
from urllib3.util import parse_url

from module.network import RequestContent
from module.utils import gen_poster_path

# TODO:改进official_title 作为标识, tmdb有id, mikan也有bangumi id

class WebPage(ABC):
    """
    Abstract class for anime info web page.
    """

    @abstractmethod
    async def get_content(self, homepage: str):
        pass


class RemoteMikan(WebPage):
    def __init__(self, url: str):
        self.content = None
        self.url = url

    async def get_content(self) -> str:
        await self._get_on_demand()
        return self.content

    async def _get_on_demand(self):
        if self.content is None:
            async with RequestContent() as req:
                self.content = await req.get_html(self.url)


class BaseParser(ABC):

    @abstractmethod
    async def parser(self):
        pass

    @abstractmethod
    async def poster_parser(self):
        pass


class MikanParser:

    def __init__(self, homepage: str, page: WebPage = RemoteMikan):
        self.page = page(homepage)
        self.homepage = homepage
        self.root_path = parse_url(homepage).host

    async def parser(self):
        content = await self.page.get_content()
        soup = BeautifulSoup(content, "html.parser")
        official_title = soup.select_one('p.bangumi-title a[href^="/Home/Bangumi/"]')
        if official_title:
            official_title = official_title.text
            official_title = re.sub(r"第.*季", "", official_title).strip()
        else:
            official_title = ""
        return official_title

    async def poster_parser(self):
        poster_link = ""
        content = await self.page.get_content()
        soup = BeautifulSoup(content, "html.parser")
        poster_div = soup.find("div", {"class": "bangumi-poster"}).get("style")
        if poster_div:
            poster_path = poster_div.split("url('")[1].split("')")[0]
            poster_link = f"https://{self.root_path}{poster_path}"
            poster_link = gen_poster_path(poster_link)

            # async with RequestContent() as req:
            #     img = await req.get_content(f"https://{self.root_path}{poster_path}")
            # suffix = poster_path.split(".")[-1]
            # poster_link = save_image(img, suffix)
        return poster_link


if __name__ == "__main__":
    import asyncio

    url = "https://mikanani.me/Home/Episode/159c273a085cc97d0cde5f4a2893aea5af7599e7"

    parser = MikanParser(url)

    print(asyncio.run(parser.poster_parser()))
