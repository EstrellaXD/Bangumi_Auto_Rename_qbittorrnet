"""config 的主要思路:
setting 会读取所有的配置,不管是不是自已需要的
不变的配置会在 setting 里放,不变是指不会有很多类型的, downloader 就会有很多种,
不常用的由 插件 自已从 setting 里面读
没有时自已将 setting 里加入自已的默认值
"""

import json
import logging
import os
from pathlib import Path
from typing import Any, Callable

from dotenv import load_dotenv
from pydantic import BaseModel

from module.models.config import Config
from module.utils.config import deep_update

from .const import ENV_TO_ATTR

logger = logging.getLogger(__name__)

try:
    from module.__version__ import VERSION
except ImportError:
    logger.info("Can't find version info, use DEV_VERSION instead")
    VERSION = "DEV_VERSION"

CONFIG_ROOT = Path("config")
CONFIX_NAME = "config.json" if VERSION != "DEV_VERSION" else "config_dev.json"
CONFIG_PATH = (CONFIG_ROOT / CONFIX_NAME).resolve()


def model_dump(
    model: BaseModel,
    include: set[str] | None = None,
    exclude: set[str] | None = None,
    by_alias: bool = False,
    exclude_unset: bool = False,
    exclude_defaults: bool = False,
    exclude_none: bool = False,
) -> dict[str, Any]:
    return model.dict(
        include=include,
        exclude=exclude,
        by_alias=by_alias,
        exclude_unset=exclude_unset,
        exclude_defaults=exclude_defaults,
        exclude_none=exclude_none,
    )


# 判断给定的 data 的 key 是否在 setting 中
def check_config_key(
    data: dict | BaseModel, updated_data: BaseModel, config_name: str
) -> bool:
    if isinstance(data, BaseModel):
        data = data.dict()
    updated_data = updated_data.dict()
    if set(updated_data.keys()) != set(data.keys()):
        return False
    return True


def get_plugin_config(config: BaseModel, config_name: str) -> BaseModel:
    """从全局配置获取当前插件需要的配置项，更新 data 中的缺失项。"""
    globel_data = model_dump(settings)
    # print(f"globel_data: {globel_data}")
    data = globel_data.get(config_name, {})
    # data 可能是 dict 和 BaseModel 的实例
    # print(f"data: {data}")
    updated_data = update_config(config, data)
    # 如果更新后的数据是默认的，更新settings
    if not check_config_key(data, updated_data, config_name):
        update_config(settings, {config_name: updated_data})
        settings.save()

    return type_validate_python(config, updated_data)


def type_validate_python(type_: BaseModel, data: Any) -> BaseModel:
    """Validate data with given type, checking required fields exist."""
    validated_data = type_.__class__.validate(data)

    return validated_data


def update_config(baseconfig: BaseModel | dict, data: dict):
    """更新 baseconfig 的配置
    传入的有俩种类型,一种是 BaseModel 的实例,一种是 dict
    BaseModel 类型的是 settings 的配置, dict 类型的是插件的配置
    """
    # 部份更新 Config
    # # 获取 baseconfig 的当前字段数据
    # print("--------------------------------")
    # print("baseconfig", baseconfig)
    # print("data", data)
    # print(f"type(baseconfig): {type(baseconfig)}")
    # print(f"type(data): {type(data)}")
    if isinstance(baseconfig, BaseModel):
        updated_data = baseconfig.dict()
        updated_data = deep_update(updated_data, data)
        updated_instance = baseconfig.__class__.validate(updated_data)
        updata_dict = updated_instance.dict()
    else:
        # 当 baseconfig 是 dict 类型时, 直接更新
        updated_data = baseconfig
        updated_data = deep_update(updated_data, data)
        updata_dict = updated_data

    # 合并传入的 data 数据

    # 验证合并后的数据并创建一个新的实例
    # 将新实例中的字段更新到 baseconfig 实例中
    for k, v in updata_dict.items():
        if hasattr(baseconfig, k):
            sub_config_obj = getattr(baseconfig, k)
            if isinstance(sub_config_obj, BaseModel) and isinstance(v, dict):
                v = update_config(sub_config_obj, v)
            elif isinstance(sub_config_obj, dict) and isinstance(v, dict):
                v = deep_update(sub_config_obj, v)
        setattr(baseconfig, k, v)

    return baseconfig


class Settings(Config):

    # def __init__(self):
    #     super().__init__()
    def __init__(self, **data):
        super().__init__(**data)
        if not data:
            if CONFIG_PATH.exists():
                self.load()
                self.save()
            else:
                self.init()

    def load(self):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config = json.load(f)
        update_config(self, config)
        # print(self.__dict__)
        # config_obj = Config.model_validate(config)

        # self.__dict__.update(config_obj.__dict__)
        logger.info("Config loaded")

    def save(self, config_dict: dict | None = None):
        if not config_dict:
            config_dict = self.dict()
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config_dict, f, indent=4, ensure_ascii=False)

    def init(self):
        load_dotenv(".env")
        self.__load_from_env()
        self.save()

    def __load_from_env(self):
        config_dict = self.dict()
        for key, section in ENV_TO_ATTR.items():
            for env, attr in section.items():
                if env in os.environ:
                    if isinstance(attr, list):
                        for _attr in attr:
                            # TODO: 这里会永远是 True,之后看看删了 if
                            attr_name = _attr[0] if isinstance(_attr, tuple) else _attr
                            config_dict[key][attr_name] = self.__val_from_env(
                                env, _attr
                            )
                    else:
                        attr_name = attr[0] if isinstance(attr, tuple) else attr
                        config_dict[key][attr_name] = self.__val_from_env(env, attr)
        config_obj = Config.validate(config_dict)
        self.__dict__.update(config_obj.__dict__)
        logger.info("Config loaded from env")

    def model_dump(self, **kwargs):
        return self.dict()

    @staticmethod
    def __val_from_env(env: str, attr: tuple[str, Callable[..., Any]] | str):
        if isinstance(attr, tuple):
            conv_func = attr[1]
            return conv_func(os.environ[env])
        else:
            return os.environ[env]

    @property
    def group_rules(self):
        return self.__dict__["group_rules"]


settings = Settings()
