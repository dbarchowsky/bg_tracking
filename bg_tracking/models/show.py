from peewee import *
from .base_model import BaseModel
from .validator import Validator


class Show(BaseModel):
    id = AutoField()
    code = TextField(null=True)
    title = TextField()
    season = IntegerField()

    def __unicode__(self):
        return self.title

    class Meta:
        db_table = 'show'
