from typing import Literal

from pydantic import BaseModel, Field, validator
from pydantic import ConfigDict as ConfigDict


class Program(BaseModel):
    # rss_time must be greater than 300,if less than 300,it will be set to 300
    rss_time: int = Field(default=900, description="Sleep time")
    # rename_time must be greater than 30,if less than 0,it will be set to 30
    rename_time: int = Field(default=60, description="Rename times in one loop")
    webui_port: int = Field(default=7892, description="WebUI port")

    @validator("rss_time")
    def validate_rss_time(cls, v: int) -> int:
        if v < 300:
            return 300
        return v

    @validator("rename_time")
    def validate_rename_time(cls, v: int) -> int:
        if v < 30:
            return 30
        return v


class Downloader(BaseModel):
    type: str = Field(default="qbittorrent", description="Downloader type")
    path: str = Field(default="/downloads/Bangumi", description="Downloader path")
    host: str = Field("172.17.0.1:8080", alias="host", description="Downloader host")
    ssl: bool = Field(False, description="Downloader ssl")

    class Config:
        extra:str = "allow"  # This allows extra fields not defined in the model

    @validator("host", pre=True)
    def validate_host(cls, value: str) -> str:
        # 如果输入值没有以 http:// 或 https:// 开头，自动加上 http://
        if not value.startswith(("http://", "https://")):
            value = f"http://{value}"
        return value
    # username: str = Field("admin", alias="username", description="Downloader username")
    # password: str = Field(
    #     "adminadmin", alias="password", description="Downloader password"
    # )


class QbDownloader(Downloader):
    type: str = Field(default="qbittorrent", description="Downloader type")
    host: str = Field(
        default="172.17.0.1:8080", alias="host", description="Downloader host"
    )
    username: str = Field(
        default="admin", alias="username", description="Downloader username"
    )
    password: str = Field(
        default="adminadmin", alias="password", description="Downloader password"
    )
    path: str = Field(default="/downloads/Bangumi", description="Downloader path")
    ssl: bool = Field(default=False, description="Downloader ssl")


class TrDownloader(Downloader):
    type: str = Field(default="transmission", description="Downloader type")
    host_: str = Field(
        default="172.17.0.1:9091", alias="host", description="Downloader host"
    )
    username_: str = Field(
        default="admin", alias="username", description="Downloader username"
    )
    password_: str = Field(
        default="admin", alias="password", description="Downloader password"
    )
    path: str = Field(default="/downloads/Bangumi", description="Downloader path")
    ssl: bool = Field(default=False, description="Downloader ssl")


class RSSParser(BaseModel):
    enable: bool = Field(default=True, description="Enable RSS parser")
    filter: list[str] = Field(default=["720", r"\d+-\d"], description="Filter")
    language: str = "zh"


class BangumiManage(BaseModel):
    enable: bool = Field(default=True, description="Enable bangumi manage")
    eps_complete: bool = Field(default=False, description="Enable eps complete")
    rename_method: str = Field(default="pn", description="Rename method")
    group_tag: bool = Field(default=False, description="Enable group tag")
    remove_bad_torrent: bool = Field(default=False, description="Remove bad torrent")


class Log(BaseModel):
    debug_enable: bool = Field(default=False, description="Enable debug")


class Proxy(BaseModel):
    enable: bool = Field(default=False, description="Enable proxy")
    type: str = Field(default="http", description="Proxy type")
    host: str = Field(default="", description="Proxy host")
    port: int = Field(default=0, description="Proxy port")
    username: str = Field(default="", alias="username", description="Proxy username")
    password: str = Field(default="", alias="password", description="Proxy password")

    # @property
    # def username(self):
    #     return expandvars(self.username_)
    #
    # @property
    # def password(self):
    #     return expandvars(self.password_)


class Notification(BaseModel):
    enable: bool = Field(default=False, description="Enable notification")
    type: str = Field(default="telegram", description="Notification type")
    token: str = Field(default="", alias="token", description="Notification token")
    chat_id: str = Field(
        default="", alias="chat_id", description="Notification chat id"
    )

    # @property
    # def token(self):
    #     return expandvars(self.token_)
    #
    # @property
    # def chat_id(self):
    #     return expandvars(self.chat_id_)


class ExperimentalOpenAI(BaseModel):
    enable: bool = Field(False, description="Enable experimental OpenAI")
    api_key: str = Field("", description="OpenAI api key")
    api_base: str = Field(
        "https://api.openai.com/v1", description="OpenAI api base url"
    )
    api_type: Literal["azure", "openai"] = Field(
        "openai", description="OpenAI api type, usually for azure"
    )
    api_version: str = Field(
        "2023-05-15", description="OpenAI api version, only for Azure"
    )
    model: str = Field(
        "gpt-3.5-turbo", description="OpenAI model, ignored when api type is azure"
    )
    deployment_id: str = Field(
        "", description="Azure OpenAI deployment id, ignored when api type is openai"
    )


class Config(BaseModel):
    program: Program = Program()
    downloader: Downloader = Downloader()
    rss_parser: RSSParser = RSSParser()
    bangumi_manage: BangumiManage = BangumiManage()
    log: Log = Log()
    proxy: Proxy = Proxy()
    notification: Notification = Notification()

    class Config:
        extra = "allow"  # This allows extra fields not defined in the model

    # experimental_openai: ExperimentalOpenAI = ExperimentalOpenAI()

    # @override
    # def model_dump(self, *args, by_alias=True, **kwargs):
    #     return super().model_dump(*args, by_alias=by_alias, **kwargs)


if __name__ == "__main__":
    pass
    # t = Program(rss_time="1")
