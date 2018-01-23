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
    pull = IntegerField(default=0)
    overlay_count = IntegerField()
    partial = IntegerField(null=True)
    scene = IntegerField(null=False)
    scene_modifier = TextField(null=True)
    width = IntegerField()

    def format_padded_scene(self):
        """
        Returns the object's scene value padded with up to 2 zeros.
        :return: Padded scene number as a string.
        """
        return '{0:0>3}{1}'.format(self.scene,
                                   self.scene_modifier if self.scene_modifier else ''
                                   )

    def has_episode(self):
        """
        Tests if the object has a valid episode attached.
        :return: True or False
        """
        try:
            if self.episode:
                return True
        except AttributeError:
            return False
        except Episode.DoesNotExist:
            return False

    def has_location(self):
        """
        Tests if the object has a valid location attached.
        :return: True or False
        """
        try:
            if self.location:
                return True
        except AttributeError:
            return False
        except Location.DoesNotExist:
            return False

    class Meta:
        db_table = 'background'
