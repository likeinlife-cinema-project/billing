from pathlib import Path
from typing import Generic, TypeVar

import yaml
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class YamlHelper(Generic[T]):
    @staticmethod
    def load(yaml_path: Path) -> dict:
        with open(yaml_path, "r") as file_obj:
            return yaml.safe_load(file_obj)

    @classmethod
    def transform_to_pydantic(cls, pydantic_model: type[T], yaml_path: Path) -> T:
        return pydantic_model(**cls.load(yaml_path))
