import os

import django
import structlog
import typer

from cli.config import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup(set_prefix=True)
router = typer.Typer(help="Commands with notification admin service")
logger = structlog.get_logger()


@router.command(help="Create templates")
def create_templates():
    from notifications.models import Template

    for ele in settings.templates:
        template = Template(**ele)
        template.save()
