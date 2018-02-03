from peewee import *
from .base_model import BaseModel


class Location(BaseModel):
    id = AutoField()
    name = TextField(unique=True)

    class Meta:
        db_table = 'location'
