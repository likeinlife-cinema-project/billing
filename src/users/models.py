from django.db import models
from models_mixins import UUIDMixin


class User(UUIDMixin, models.Model):
    pass
