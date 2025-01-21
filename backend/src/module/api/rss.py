from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from module.manager import SeasonCollector
from module.models import (
    APIResponse,
    Bangumi,
    ResponseModel,
    RSSItem,
    RSSUpdate,
    Torrent,
)
from module.rss import RSSAnalyser, RSSEngine, RSSManager, RSSRefresh
from module.security.api import UNAUTHORIZED, get_current_user

from .response import u_response

router = APIRouter(prefix="/rss", tags=["rss"])
engine = RSSEngine()
analyser = RSSAnalyser()
collector = SeasonCollector()


@router.get(
    path="", response_model=list[RSSItem], dependencies=[Depends(get_current_user)]
)
async def get_rss():
    return RSSManager().search_all()


@router.post(
    path="/add", response_model=APIResponse, dependencies=[Depends(get_current_user)]
)
async def add_rss(rss: RSSItem):
    manager = RSSManager()
    res = await manager.add_rss(rss.url, rss.name, rss.aggregate, rss.parser)
    if res:
        result = ResponseModel(
            status=True,
            status_code=200,
            msg_en="RSS added successfully.",
            msg_zh="RSS 添加成功。",
        )
    else:
        result = ResponseModel(
            status=False,
            status_code=406,
            msg_en="Failed to get RSS title.",
            msg_zh="无法获取 RSS 标题。",
        )

    return u_response(result)


@router.post(
    path="/enable/many",
    response_model=APIResponse,
    dependencies=[Depends(get_current_user)],
)
async def enable_many_rss(
    rss_ids: list[int],
):
    result = RSSManager().enable_list(rss_ids)

    result = ResponseModel(
        status=True,
        status_code=200,
        msg_en="Enable RSS successfully.",
        msg_zh="启用 RSS 成功。",
    )

    return u_response(result)


@router.delete(
    path="/delete/{rss_id}",
    response_model=APIResponse,
    dependencies=[Depends(get_current_user)],
)
async def delete_rss(rss_id: int):
    if RSSManager().delete(rss_id):
        return JSONResponse(
            status_code=200,
            content={
                "msg_en": "Delete RSS successfully.",
                "msg_zh": "删除 RSS 成功。",
            },
        )
    else:
        return JSONResponse(
            status_code=406,
            content={"msg_en": "Delete RSS failed.", "msg_zh": "删除 RSS 失败。"},
        )


@router.post(
    path="/delete/many",
    response_model=APIResponse,
    dependencies=[Depends(get_current_user)],
)
async def delete_many_rss(
    rss_ids: list[int],
):
    result = RSSManager().delete_list(rss_ids)
    result = ResponseModel(
        status=True,
        status_code=200,
        msg_en="Delete RSS successfully.",
        msg_zh="删除 RSS 成功。",
    )
    return u_response(result)


@router.patch(
    path="/disable/{rss_id}",
    response_model=APIResponse,
    dependencies=[Depends(get_current_user)],
)
async def disable_rss(rss_id: int):
    if RSSManager().disable(rss_id):
        return JSONResponse(
            status_code=200,
            content={
                "msg_en": "Disable RSS successfully.",
                "msg_zh": "禁用 RSS 成功。",
            },
        )
    else:
        return JSONResponse(
            status_code=406,
            content={"msg_en": "Disable RSS failed.", "msg_zh": "禁用 RSS 失败。"},
        )


@router.post(
    path="/disable/many",
    response_model=APIResponse,
    dependencies=[Depends(get_current_user)],
)
async def disable_many_rss(rss_ids: list[int]):
    RSSManager().disable_list(rss_ids)
    result = ResponseModel(
        status=True,
        status_code=200,
        msg_en="Disable RSS successfully.",
        msg_zh="禁用 RSS 成功。",
    )

    return u_response(result)


@router.patch(
    path="/update/{rss_id}",
    response_model=APIResponse,
    dependencies=[Depends(get_current_user)],
)
async def update_rss(
    rss_id: int, data: RSSUpdate, current_user=Depends(get_current_user)
):
    if not current_user:
        raise UNAUTHORIZED
    if RSSManager().update(rss_id, data):
        return JSONResponse(
            status_code=200,
            content={
                "msg_en": "Update RSS successfully.",
                "msg_zh": "更新 RSS 成功。",
            },
        )
    else:
        return JSONResponse(
            status_code=406,
            content={"msg_en": "Update RSS failed.", "msg_zh": "更新 RSS 失败。"},
        )


@router.get(
    path="/refresh/all",
    response_model=APIResponse,
    dependencies=[Depends(get_current_user)],
)
async def refresh_all():
    await engine.refresh_all_rss()
    return JSONResponse(
        status_code=200,
        content={
            "msg_en": "Refresh all RSS successfully.",
            "msg_zh": "刷新 RSS 成功。",
        },
    )


@router.get(
    path="/refresh/{rss_id}",
    response_model=APIResponse,
    dependencies=[Depends(get_current_user)],
)
async def refresh_rss(rss_id: int):
    await engine.refresh_rss(rss_id=rss_id)
    return JSONResponse(
        status_code=200,
        content={
            "msg_en": "Refresh RSS successfully.",
            "msg_zh": "刷新 RSS 成功。",
        },
    )


@router.get(
    path="/torrent/{rss_id}",
    response_model=list[Torrent],
    dependencies=[Depends(get_current_user)],
)
async def get_torrent(
    rss_id: int,
):
    return RSSManager().get_rss_torrents(rss_id)


@router.post(
    "/analysis", response_model=Bangumi, dependencies=[Depends(get_current_user)]
)
async def analysis(rss: RSSItem):
    torrents = await RSSRefresh(rss).pull_rss()
    if not torrents:
        return u_response(
            ResponseModel(
                status=False,
                status_code=406,
                msg_en="Cannot find any torrent.",
                msg_zh="无法找到种子。",
            )
        )
    # 只有非聚合才会用
    for torrent in torrents:
        data = await analyser.torrent_to_data(torrent, rss)
        if data:
            return data

    return u_response(
        ResponseModel(
            status=False,
            status_code=406,
            msg_en="Cannot parse this link.",
            msg_zh="无法解析此链接。",
        )
    )
    # data = await analyser.link_to_data(rss)
    # if isinstance(data, Bangumi):
    #     return data
    # else:
    #     return u_response(data)


@router.post(
    "/collect", response_model=APIResponse, dependencies=[Depends(get_current_user)]
)
async def download_collection(data: Bangumi):
    await engine.refresh_rss(bangumi=data)
    # TODO: resp 要等后面统一改
    resp = True

    if resp:
        resp = ResponseModel(
            status=True,
            status_code=200,
            msg_en=f"Collections of {data.official_title} Season {data.season} completed.",
            msg_zh=f"收集 {data.official_title} 第 {data.season} 季完成。",
        )
    else:
        resp = ResponseModel(
            status=False,
            status_code=406,
            msg_en=f"Collection of {data.official_title} Season {data.season} failed.",
            msg_zh=f"收集 {data.official_title} 第 {data.season} 季失败, 种子已经添加。",
        )
    return u_response(resp)


@router.post(
    "/subscribe",
    response_model=APIResponse,
    dependencies=[Depends(get_current_user)],
)
async def subscribe(data: Bangumi, rss: RSSItem):
    await collector.subscribe_season(data, parser=rss.parser)
    resp = True
    if resp:
        resp = ResponseModel(
            status=True,
            status_code=200,
            msg_en=f"[Engine] Download {data.official_title} successfully.",
            msg_zh=f"下载 {data.official_title} 成功。",
        )
    else:
        resp = ResponseModel(
            status=False,
            status_code=406,
            msg_en=f"[Engine] Download {data.official_title} failed.",
            msg_zh=f"[Engine] 下载 {data.official_title} 失败。",
        )
    return u_response(resp)
