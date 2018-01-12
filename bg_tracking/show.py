from peewee import *
from .base_model import BaseModel


class Show(BaseModel):
    code = TextField(null=True)
    name = TextField()
    season = IntegerField()

    class Meta:
        db_table = 'show'
