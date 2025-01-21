import re
import time
from dataclasses import dataclass

from module.conf import TMDB_API
from module.network import RequestContent
from module.utils import gen_poster_path

TMDB_URL = "https://api.themoviedb.org"
TMDB_IMG_URL = "https://image.tmdb.org/t/p/w780"


@dataclass
class TMDBInfo:
    id: int
    title: str
    original_title: str
    season: list[dict]
    last_season: int
    year: str
    poster_link: str | None = None


@dataclass
class ShowInfo:
    adult: bool
    backdrop_path: str
    genre_ids: list[int]
    id: int
    origin_country: list[str]
    original_language: str
    original_name: str
    overview: str
    popularity: float
    poster_path: str
    first_air_date: str
    name: str
    vote_average: float
    vote_count: int


@dataclass
class Genre:
    id: int
    name: str


@dataclass
class Network:
    id: int
    logo_path: str | None
    name: str
    origin_country: str


@dataclass
class LastEpisodeToAir:
    id: int
    name: str
    overview: str
    vote_average: float
    vote_count: int
    air_date: str
    episode_number: int
    episode_type: str
    production_code: str
    runtime: int
    season_number: int
    show_id: int
    still_path: str

@dataclass
class ProductionCompany:
    id: int
    name: str
    origin_country: str
    logo_path: str | None = None

@dataclass
class Season:
    air_date: str | None
    episode_count: int
    id: int
    name: str
    overview: str
    season_number: int
    vote_average: float
    poster_path: str | None = None

@dataclass
class TVShow:
    adult: bool
    backdrop_path: str
    created_by: list[dict]
    episode_run_time: list[int]
    first_air_date: str
    genres: list[Genre]
    homepage: str
    id: int
    in_production: bool
    languages: list[str]
    last_air_date: str
    last_episode_to_air: LastEpisodeToAir
    name: str
    networks: list[Network]
    number_of_episodes: int
    number_of_seasons: int
    origin_country: list[str]
    original_language: str
    original_name: str
    overview: str
    popularity: float
    poster_path: str
    production_companies: list[ProductionCompany]
    production_countries: list[dict[str, str]]
    seasons: list[Season]
    next_episode_to_air: str | None = None


LANGUAGE = {"zh": "zh-CN", "jp": "ja-JP", "en": "en-US"}


def search_url(e):
    return f"{TMDB_URL}/3/search/tv?api_key={TMDB_API}&page=1&query={e}&include_adult=false"


def info_url(e, key):
    return f"{TMDB_URL}/3/tv/{e}?api_key={TMDB_API}&language={LANGUAGE[key]}"


async def is_animation(genre_ids: list[int]) -> bool:
    # grnres_id 内有, 不用再请求一次
    #
    if 16 in genre_ids:
        return True
    return False


def get_season(seasons: list[dict[str, str]]) -> tuple[int, str]:
    # sort by season number
    ss = [s for s in seasons if s["air_date"] is not None and s["season"]]
    ss = sorted(ss, key=lambda e: e.get("air_date"), reverse=True)
    for season in ss:
        date = season.get("air_date").split("-")
        [year, _, _] = date
        now_year = time.localtime().tm_year
        if int(year) <= now_year:
            return int(season.get("season")), season.get("poster_path")
    return len(ss), ss[-1].get("poster_path")


async def tmdb_parser(title: str, language: str, test: bool = False) -> TMDBInfo | None:
    async with RequestContent() as req:
        url = search_url(title)
        json_contents = await req.get_json(url)
        contents: list[ShowInfo] = json_contents.get("results", "")
        # TODO: 还是怪怪的
        if contents and len(contents) == 0:
            url = search_url(title.replace(" ", ""))
            json_contents = await req.get_json(url)
            contents: list[ShowInfo] = json_contents.get("results", "")
        # # 判断动画
        if contents:
            sorted_contents = sorted(
                contents, key=lambda e: e.get("first_air_date"), reverse=True
            )
            for content in sorted_contents:
                genre_ids: list[int] = content["genre_ids"]
                if await is_animation(genre_ids):
                    # 类似狼与香辛料, 会存在多个结果,但动画前面的就覆盖了
                    # TODO: sort by time?
                    break
            url_info = info_url(content["id"], language)
            info_content = await req.get_json(url_info)

            season = [
                {
                    "season": s.get("season_number"),
                    "air_date": s.get("air_date"),
                    "poster_path": s.get("poster_path"),
                }
                for s in info_content.get("seasons")
            ]
            last_season, poster_path = get_season(season)
            # TODO: 什么情况会是 None?
            if poster_path is None:
                poster_path: str = info_content.get("poster_path")

            original_title: str = info_content.get("original_name")
            official_title: str = info_content.get("name")
            year_number = info_content.get("first_air_date").split("-")[0]
            poster_link = None
            if poster_path:
                poster_link = f"{TMDB_IMG_URL}{poster_path}"
                poster_link = gen_poster_path(poster_link)

            return TMDBInfo(
                id,
                official_title,
                original_title,
                season,
                last_season,
                str(year_number),
                poster_link,
            )
        else:
            return None


if __name__ == "__main__":
    import asyncio

    ans = asyncio.run(tmdb_parser("狼与香辛料", "zh"))
    print(ans)
