from peewee import *
from playhouse.sqlite_ext import PrimaryKeyAutoIncrementField
from .base_model import BaseModel


class Location(BaseModel):
    id = PrimaryKeyAutoIncrementField()
    name = TextField(unique=True)

    class Meta:
        db_table = 'location'
