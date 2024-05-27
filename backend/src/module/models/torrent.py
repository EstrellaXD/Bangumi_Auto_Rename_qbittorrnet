from typing import Optional

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class Torrent(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, alias="id")
    bangumi_id: Optional[int] = Field(None, alias="refer_id", foreign_key="bangumi.id")
    rss_id: Optional[int] = Field(None, alias="rss_id", foreign_key="rssitem.id")
    name: str = Field("", alias="name")
    url: str = Field("https://example.com/torrent", alias="url")
    homepage: Optional[str] = Field(None, alias="homepage")
    downloaded: bool = Field(False, alias="downloaded")
    hash: Optional[str] = Field(None, alias="hash")


class TorrentUpdate(SQLModel):
    downloaded: bool = Field(False, alias="downloaded")


class EpisodeFile(BaseModel):
    media_path: str = Field(...)
    group: str | None = Field(None)
    title: str = Field(...)
    season: int = Field(...)
    episode: int = Field(None)
    suffix: str = Field(..., regex=r"\.(mkv|mp4|MKV|MP4)$")


class SubtitleFile(BaseModel):
    media_path: str = Field(...)
    group: str | None = Field(None)
    title: str = Field(...)
    season: int = Field(...)
    episode: int = Field(None)
    language: str = Field(..., regex=r"(zh|zh-tw)")
    suffix: str = Field(..., regex=r"\.(ass|srt|ASS|SRT)$")
