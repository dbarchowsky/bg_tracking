from peewee import *
from .base_model import BaseModel
from .show import Show


class Episode(BaseModel):
    id = AutoField()
    title = CharField()
    number = IntegerField()
    show = ForeignKeyField(Show, db_column='show_id', to_field='id', backref='episodes')

    def format_padded_number(self):
        return '%03d' % self.number

    def __unicode__(self):
        return "{} {}".format(self.format_padded_number(), self.title)

    class Meta:
        db_table = 'episode'
