import logging
import os
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from module.api import lifespan, v1
from module.conf import VERSION, settings, setup_logger
from module.utils import load_image

setup_logger(reset=True)
logger = logging.getLogger(__name__)
uvicorn_logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": logger.handlers,
    "loggers": {
        "uvicorn": {
            "level": logger.level,
        },
        "uvicorn.access": {
            "level": "WARNING",
        },
    },
}


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    # mount routers
    app.include_router(v1, prefix="/api")

    return app


app = create_app()


@app.get("/posters/{path:path}", tags=["posters"])
async def posters(path: str):
    # TODO: 肯定在这里是不合适的
    post_path = Path("data/posters") / path
    if not post_path.exists():
        await load_image(path)
    return FileResponse(post_path)


if VERSION != "DEV_VERSION":
    app.mount("/assets", StaticFiles(directory="dist/assets"), name="assets")
    app.mount("/images", StaticFiles(directory="dist/images"), name="images")
    # app.mount("/icons", StaticFiles(directory="dist/icons"), name="icons")
    templates = Jinja2Templates(directory="dist")

    @app.get("/{path:path}")
    def html(request: Request, path: str):
        files = os.listdir("dist")
        if path in files:
            return FileResponse(f"dist/{path}")
        else:
            context = {"request": request}
            return templates.TemplateResponse("index.html", context)
else:
    @app.get("/", status_code=302, tags=["html"])
    def index():
        return RedirectResponse("/docs")


if __name__ == "__main__":
    if os.getenv("IPV6"):
        host = "::"
    else:
        host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run(
        app,
        host=host,
        port=settings.program.webui_port,
        log_config=uvicorn_logging_config,
    )
