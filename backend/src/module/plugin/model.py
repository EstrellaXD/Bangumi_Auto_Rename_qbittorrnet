"""本模块定义插件相关信息。

FrontMatter:
    sidebar_position: 3
    description: nonebot.plugin.model 模块
"""

import contextlib
from dataclasses import dataclass, field
from types import ModuleType
from typing import TYPE_CHECKING, Any

from nonebot.utils import resolve_dot_notation
from pydantic import BaseModel

if TYPE_CHECKING:
    from nonebot.adapters import Adapter

    from .manager import PluginManager


@dataclass(eq=False)
class PluginMetadata:
    """插件元信息，由插件编写者提供"""

    name: str
    """插件名称"""
    description: str
    """插件功能介绍"""
    usage: str
    """插件使用方法"""
    homepage: str | None = None
    """插件主页"""
    config: type[BaseModel] | None = None  # noqa: UP006
    """插件配置项"""
    extra: dict[Any, Any] = field(default_factory=dict)
    """插件额外信息，可由插件编写者自由扩展定义"""


@dataclass(eq=False)
class Plugin:
    """存储插件信息"""

    name: str
    """插件名称，NoneBot 使用 文件/文件夹 名称作为插件名称"""
    module: ModuleType
    """插件模块对象"""
    module_name: str
    """点分割模块路径"""
    manager: "PluginManager"
    """导入该插件的插件管理器"""
    parent_plugin: "Plugin" | None = None
    """父插件"""
    sub_plugins: set["Plugin"] = field(default_factory=set)
    """子插件集合"""
    metadata: PluginMetadata | None = None

    @property
    def id_(self) -> str:
        """插件索引标识"""
        return (
            f"{self.parent_plugin.id_}:{self.name}" if self.parent_plugin else self.name
        )
