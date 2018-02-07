from peewee import *
from .base_model import BaseModel
from .show import Show


class Episode(BaseModel):
    id = AutoField()
    title = CharField()
    number = IntegerField()
    show = ForeignKeyField(Show, db_column='show_id', to_field='id', backref='episodes', on_delete='CASCADE')

    def format_padded_number(self):
        return '%03d' % self.number

    def __str__(self):
        if type(self.show) is Show and self.show.code:
            return "{}-{} “{}”".format(self.show.code, self.format_padded_number(), self.title)
        else:
            return "{} “{}”".format(self.format_padded_number(), self.title)

    class Meta:
        db_table = 'episode'
