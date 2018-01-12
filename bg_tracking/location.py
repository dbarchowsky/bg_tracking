from peewee import *
from .base_model import BaseModel


class Location(BaseModel):
    name = TextField(unique=True)

    class Meta:
        db_table = 'location'
