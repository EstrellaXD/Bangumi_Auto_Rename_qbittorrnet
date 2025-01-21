from typing import Any, TypeVar
from pydantic import BaseModel

K = TypeVar("K")
def deep_update(
    mapping: dict[K, Any], *updating_mappings: dict[K, Any]
) -> dict[K, Any]:
    """深度更新合并字典"""
    updated_mapping = mapping.copy()
    for updating_mapping in updating_mappings:
        for k, v in updating_mapping.items():
            if (
                k in updated_mapping
                and isinstance(updated_mapping[k], dict)
            ):
                if isinstance(v, dict):
                    updated_mapping[k] = deep_update(updated_mapping[k], v)
                if isinstance(v, BaseModel):
                    updated_mapping[k] = deep_update(updated_mapping[k], v.dict())
            else:
                updated_mapping[k] = v
    return updated_mapping


