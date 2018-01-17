from peewee import *
from playhouse.sqlite_ext import PrimaryKeyAutoIncrementField
from .base_model import BaseModel
from .validator import Validator


class Show(BaseModel):
    id = PrimaryKeyAutoIncrementField()
    code = TextField(null=True)
    title = TextField()
    season = IntegerField()

    def collect_form_data(self, form):
        """Validates form data
        Args:
            form (dict): Form data
        """
        error = ''
        error += self.collect_request_int(form, 'id')
        error += self.collect_request_string(form, 'title')
        error += self.collect_request_int(form, 'season')
        error += self.collect_request_string(form, 'code')
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
            error += 'Show name is required. \n'
        if not Validator.is_non_zero_int_value(self.season):
            error += 'Show season is required. \n'
        if len(error) > 0:
            raise ValueError(error)

    class Meta:
        db_table = 'show'
