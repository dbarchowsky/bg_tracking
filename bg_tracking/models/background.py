from peewee import *
from playhouse.sqlite_ext import PrimaryKeyAutoIncrementField
from .base_model import BaseModel
from .episode import Episode
from .location import Location
from .validator import Validator


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

    def collect_form_data(self, form):
        """Validates form data
        Args:
            form (dict): Form data
        """
        error = ''
        error += self.collect_request_int(form, 'id')
        error += self.collect_request_int(form, 'episode')
        error += self.collect_request_int(form, 'scene')
        error += self.collect_request_string(form, 'scene_modifier')
        error += self.collect_request_int(form, 'width')
        error += self.collect_request_int(form, 'height')
        error += self.collect_request_int(form, 'overlay_count')
        error += self.collect_request_bool(form, 'establishing_shot')
        error += self.collect_request_bool(form, 'pull')
        error += self.collect_request_int(form, 'location')
        error += self.collect_request_float(form, 'hours')
        error += self.collect_request_date(form, 'date_started')
        error += self.collect_request_date(form, 'date_finished')
        error += self.collect_request_bool(form, 'approved')
        if len(error) > 0:
            raise ValueError(error)

    def validate_form_data(self):
        """Validates form data
        """
        error = ''
        if self.id:
            if not Validator.is_integer(self.id):
                error += 'Invalid id value. \n'
        if not Validator.is_non_empty_string(self.title):
            error += 'Show title is required. \n'
        if not Validator.is_non_zero_int_value(self.season):
            error += 'Show season is required. \n'
        if len(error) > 0:
            raise ValueError(error)

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
