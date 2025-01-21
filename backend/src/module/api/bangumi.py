from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.util.concurrency import asyncio

from module.database import Database, engine
from module.manager import TorrentManager
from module.models import APIResponse, Bangumi, BangumiUpdate, ResponseModel
from module.security.api import get_current_user

from .response import u_response

router = APIRouter(prefix="/bangumi", tags=["bangumi"])


def str_to_list(data: Bangumi):
    data.filter = data.filter.split(",")
    data.rss_link = data.rss_link.split(",")
    return data


@router.get(
    "/get/all", response_model=list[Bangumi], dependencies=[Depends(get_current_user)]
)
async def get_all_data():
    with Database() as db:
        return db.bangumi.search_all()


@router.get(
    "/get/{bangumi_id}",
    response_model=Bangumi,
    dependencies=[Depends(get_current_user)],
)
async def get_data(bangumi_id: str):
    resp = TorrentManager().search_one(bangumi_id)
    return resp


@router.patch(
    "/update/{bangumi_id}",
    response_model=APIResponse,
    dependencies=[Depends(get_current_user)],
)
async def update_rule(
    bangumi_id: int,
    data: BangumiUpdate,
):
    resp = await TorrentManager().update_rule(bangumi_id, data)
    if resp:
        resp = ResponseModel(
            status_code=200,
            status=True,
            msg_en=f"Update rule for {data.official_title}",
            msg_zh=f"更新 {data.official_title} 规则",
        )

    else:
        resp = ResponseModel(
            status_code=406,
            status=False,
            msg_en=f"Can't find data with {bangumi_id}",
            msg_zh=f"无法找到 id {bangumi_id} 的数据",
        )
    return u_response(resp)


@router.delete(
    path="/delete/{bangumi_id}",
    response_model=APIResponse,
    dependencies=[Depends(get_current_user)],
)
async def delete_rule(bangumi_id: str, file: bool = False):
    data,torrent_message = await TorrentManager().delete_rule(bangumi_id, file)
    if data:
        resp =  ResponseModel(
            status_code=200,
            status=True,
            msg_en=f"Delete rule for {data.official_title}. {torrent_message.msg_en if file else ''}",
            msg_zh=f"删除 {data.official_title} 规则。{torrent_message.msg_zh if file else ''}",
        )
    else:
        resp = ResponseModel(
                status_code=406,
                status=False,
                msg_en=f"Can't find id {bangumi_id}",
                msg_zh=f"无法找到 id {bangumi_id}",
            )
    return u_response(resp)


@router.delete(
    path="/delete/many/",
    response_model=APIResponse,
    dependencies=[Depends(get_current_user)],
)
async def delete_many_rule(bangumi_id: list, file: bool = False):
    tasks = []
    for i in bangumi_id:
        tasks.append(TorrentManager().delete_rule(i, file))

    resp = await asyncio.gather(*tasks)
    resp = resp[0]
    return u_response(resp)


@router.delete(
    path="/disable/{bangumi_id}",
    response_model=APIResponse,
    dependencies=[Depends(get_current_user)],
)
async def disable_rule(bangumi_id: str, file: bool = False):
    resp = await TorrentManager().disable_rule(bangumi_id, file)
    return u_response(resp)


@router.delete(
    path="/disable/many/",
    response_model=APIResponse,
    dependencies=[Depends(get_current_user)],
)
async def disable_many_rule(bangumi_id: list, file: bool = False):
    tasks = []
    for i in bangumi_id:
        tasks.append(TorrentManager().disable_rule(i, file))
    resp = await asyncio.gather(*tasks)
    resp = resp[-1]
    return u_response(resp)


@router.get(
    path="/enable/{bangumi_id}",
    response_model=APIResponse,
    dependencies=[Depends(get_current_user)],
)
async def enable_rule(bangumi_id: str):
    resp = await TorrentManager().enable_rule(bangumi_id)
    return u_response(resp)


@router.get(
    path="/refresh/poster/all",
    response_model=APIResponse,
    dependencies=[Depends(get_current_user)],
)
async def refresh_poster():
    resp = await TorrentManager().refresh_poster()
    return u_response(resp)


@router.get(
    path="/refresh/poster/{bangumi_id}",
    response_model=APIResponse,
    dependencies=[Depends(get_current_user)],
)
async def refresh_single_poster(bangumi_id: int):
    resp = await TorrentManager().refind_poster(bangumi_id)
    return u_response(resp)


@router.get(
    "/reset/all", response_model=APIResponse, dependencies=[Depends(get_current_user)]
)
async def reset_all():
    with Database(engine) as db:
        db.bangumi.delete_all()
        return JSONResponse(
            status_code=200,
            content={
                "msg_en": "Reset all rules successfully.",
                "msg_zh": "重置所有规则成功。",
            },
        )
