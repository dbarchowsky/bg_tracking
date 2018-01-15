from peewee import *
from .base_model import BaseModel
from .validator import Validator


class Show(BaseModel):
    code = TextField(null=True)
    name = TextField()
    season = IntegerField()


    def collect_form_data(self, form):
        """Validates form data
        Args:
            form (dict): Form data
        """
        error = ''
        error += self.collect_request_var(form, 'id')
        error += self.collect_request_var(form, 'name')
        error += self.collect_request_var(form, 'season')
        error += self.collect_request_var(form, 'code')
        if len(error) > 0:
            raise ValueError(error)


    def validate_form_data(self, form):
        """Validates form data
        Args:
            form (dict): Form data
        """
        error = ''
        if self.id:
            if not Validator.is_integer(self.id):
                error += 'Invalid id value. \n'
        if not Validator.is_non_empty_string(self.name):
            error += 'Show name is required. \n'
        if not Validator.validate_non_zero_int_value(self.season):
            error += 'Show season is required. \n'
        if len(error) > 0:
            raise ValueError(error)


    class Meta:
        db_table = 'show'
