from json import load

import structlog

from pydantic_settings import BaseSettings


logger = structlog.get_logger()


class TemplateSettings(BaseSettings):
    @property
    def templates(self):
        with open("./cli/templates.json", "r") as file:
            templates = load(file)
            return templates


settings = TemplateSettings()
