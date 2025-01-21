from sqlmodel import Field, SQLModel


class RSSItem(SQLModel, table=True):
    """
        主码是 rss_link
        id 是前端用的
    """
    id: int = Field(default=None, primary_key=True, alias="id")
    name: str|None = Field(default=None, alias="name")
    url: str = Field(default="https://mikanani.me", alias="url")
    aggregate: bool = Field(default=False, alias="aggregate")
    parser: str = Field(default="mikan", alias="parser")
    enabled: bool = Field(default=True, alias="enabled")


class RSSUpdate(SQLModel):
    name: str|None = Field(default=None, alias="name")
    url: str|None = Field(default="https://mikanani.me", alias="url")
    aggregate: bool|None = Field(default=True, alias="aggregate")
    parser: str|None = Field(default="mikan", alias="parser")
    enabled: bool|None = Field(default=True, alias="enabled")
