from peewee import *
from .base_model import BaseModel
from .show import Show


class Episode(BaseModel):
    name = TextField()
    number = IntegerField()
    show = ForeignKeyField(db_column='show_id', rel_model=Show, to_field='id')

    def format_padded_number(self):
        return '%03d' % self.number

    class Meta:
        db_table = 'episode'
