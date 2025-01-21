from pydantic import BaseModel, Field, validator


class Config(BaseModel):
    host: str = Field(
        default="http://172.17.0.1:8080", alias="host", description="Downloader host"
    )
    username: str = Field(
        default="admin", alias="username", description="Downloader username"
    )
    password: str = Field(
        default="adminadmin", alias="password", description="Downloader password"
    )


if __name__ == "__main__":
    host = "127.0.0.1:8999"
    print(Config(host=host, path="nnone"))
