from peewee import *
from .base_model import BaseModel
from .episode import Episode
from .location import Location


class Background(BaseModel):
    id = AutoField()
    episode = ForeignKeyField(Episode, db_column='episode_id', field='id', backref='backgrounds', on_delete='CASCADE')
    scene = IntegerField(null=False)
    scene_modifier = CharField(null=True)
    width = IntegerField()
    height = IntegerField()
    overlay_count = IntegerField()
    hours = FloatField(null=True)
    location = ForeignKeyField(Location, db_column='location_id', field='id')
    establishing_shot = BooleanField(choices=((False, 'f'), (True, 't')), null=True)
    partial = BooleanField(choices=((False, 'f'), (True, 't')), null=True)
    pull = BooleanField(choices=((False, 'f'), (True, 't')), null=True)
    card = BooleanField(choices=((False, 'f'), (True, 't')), null=True)
    date_started = DateField(null=True)
    date_finished = DateField(null=True)
    approved = BooleanField(choices=((False, 'f'), (True, 't')), null=True)

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

    def __str__(self):
        return 'Sc {}'.format(self.format_padded_scene())

    class Meta:
        db_table = 'background'
