from datetime import timedelta

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, Response
from fastapi.security import OAuth2PasswordRequestForm

from module.models import APIResponse
from module.models.user import User, UserUpdate
from module.security.api import (
    active_user,
    auth_user,
    get_current_user,
    update_user_info,
)
from module.security.jwt import create_access_token

from .response import u_response

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=dict)
async def login(response: Response, form_data=Depends(OAuth2PasswordRequestForm)):
    user = User(username=form_data.username, password=form_data.password)
    resp = auth_user(user)
    if resp.status:
        token = create_access_token(
            data={"sub": user.username}, expires_delta=timedelta(days=1)
        )
        response.set_cookie(key="token", value=token, httponly=True, max_age=86400)
        return {"access_token": token, "token_type": "bearer"}
    return u_response(resp)


@router.get(
    "/refresh_token", response_model=dict, dependencies=[Depends(get_current_user)]
)
async def refresh(response: Response):
    token = create_access_token(
        data={"sub": active_user[0]}, expires_delta=timedelta(days=1)
    )
    response.set_cookie(key="token", value=token, httponly=True, max_age=86400)
    return {"access_token": token, "token_type": "bearer"}


@router.get(
    "/logout", response_model=APIResponse, dependencies=[Depends(get_current_user)]
)
async def logout(response: Response):
    active_user.clear()
    response.delete_cookie(key="token")
    return JSONResponse(
        status_code=200,
        content={"msg_en": "Logout successfully.", "msg_zh": "登出成功。"},
    )


@router.post("/update", response_model=dict, dependencies=[Depends(get_current_user)])
async def update_user(user_data: UserUpdate, response: Response):
    old_user = active_user[0]
    if update_user_info(user_data, old_user):
        token = create_access_token(
            data={"sub": old_user}, expires_delta=timedelta(days=1)
        )
        response.set_cookie(
            key="token",
            value=token,
            httponly=True,
            max_age=86400,
        )
        return {
            "access_token": token,
            "token_type": "bearer",
            "message": "update success",
        }
