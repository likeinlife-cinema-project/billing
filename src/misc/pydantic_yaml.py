from pathlib import Path

from pydantic import BaseModel
from typing_extensions import Self

from misc.yaml_helper import YamlHelper


class YamlSettings(BaseModel):
    @classmethod
    def from_yaml(cls, yaml_path: Path) -> Self:
        return YamlHelper.transform_to_pydantic(cls, yaml_path)
