from peewee import *
from .base_model import BaseModel


class Show(BaseModel):
    id = AutoField()
    code = CharField(null=True)
    title = CharField()
    season = IntegerField()

    def __str__(self):
        if self.code:
            return '{} {} season {}'.format(self.code, self.title, self.season)
        else:
            return '{} season {}'.format(self.title, self.season)

    class Meta:
        db_table = 'show'
