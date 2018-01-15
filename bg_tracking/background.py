from peewee import *
from playhouse.sqlite_ext import PrimaryKeyAutoIncrementField
from .base_model import BaseModel
from .episode import Episode
from .location import Location


class Background(BaseModel):
    id = PrimaryKeyAutoIncrementField()
    approved = IntegerField(null=True)
    date_finished = TextField(null=True)
    date_started = TextField(null=True)
    episode = ForeignKeyField(db_column='episode_id', rel_model=Episode, to_field='id')
    establishing_shot = IntegerField(null=True)
    height = IntegerField()
    hours = FloatField(null=True)
    location = ForeignKeyField(db_column='location_id', rel_model=Location, to_field='id')
    overlay_count = IntegerField()
    partial = IntegerField(null=True)
    scene = IntegerField()
    width = IntegerField()

    def format_padded_scene(self):
        return '%03d' % self.scene

    class Meta:
        db_table = 'background'
