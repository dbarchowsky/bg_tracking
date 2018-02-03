from peewee import *
from .base_model import BaseModel


class Location(BaseModel):
    id = AutoField()
    name = TextField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'location'
