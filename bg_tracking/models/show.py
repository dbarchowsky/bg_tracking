from peewee import *
from .base_model import BaseModel
from .validator import Validator


class Show(BaseModel):
    id = AutoField()
    code = TextField(null=True)
    title = TextField()
    season = IntegerField()

    def __str__(self):
        if self.code:
            return '{} {} season {}'.format(self.code, self.title, self.season)
        else:
            return '{} season {}'.format(self.title, self.season)

    class Meta:
        db_table = 'show'
