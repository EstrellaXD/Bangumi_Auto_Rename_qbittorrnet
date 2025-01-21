from fastapi import APIRouter, Depends, Query
from sse_starlette.sse import EventSourceResponse

from module.models import Bangumi
from module.searcher import SEARCH_CONFIG, SearchTorrent
from module.security.api import UNAUTHORIZED, get_current_user

router = APIRouter(prefix="/search", tags=["search"])


@router.get(
    "/bangumi", response_model=list[Bangumi], dependencies=[Depends(get_current_user)]
)
async def search_torrents(site: str = "mikan", keywords: str = Query(None)):
    """
    Server Send Event for per Bangumi item
    """
    # TODO: 是否要大于一定才开始
    if not keywords or len(keywords) < 2:
        return []
    keywords: list[str] = keywords.split(" ")

    return EventSourceResponse(
        SearchTorrent().analyse_keyword(keywords=keywords, site=site)
    )


@router.get( "/provider", response_model=list[str], dependencies=[Depends(get_current_user)])
async def search_provider()->list[str]:
    """从配置文件中获取支持的搜索引擎
    """
    return list(SEARCH_CONFIG.keys())
