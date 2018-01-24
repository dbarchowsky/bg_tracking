from peewee import *
import os
from bg_tracking.models.validator import Validator

db = SqliteDatabase(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'bgs.db'), **{})


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    
    def collect_request_var(self, form, key):
        try:
            if len(str(form[key])) > 0:
                setattr(self, key, form[key])
        except KeyError:
            return 'Expected input is missing: {} \n'.format(key)
        return ''

    def collect_request_int(self, form, key):
        try:
            if Validator.is_integer(form[key]):
                setattr(self, key, int(form[key]))
            elif form[key] is None or form[key] == '':
                setattr(self, key, None)
            elif len(str(form[key])) > 0:
                raise ValueError('Invalid value for {}: {}'.format(key, form[key]))
            else:
                setattr(self, key, None)
        except KeyError:
            return 'Expected input is missing: {} \n'.format(key)
        return ''

    def collect_request_string(self, form, key):
        err = self.collect_request_var(form, key)
        if err == '':
            if form[key] is None or form[key] == '':
                setattr(self, key, '')
        return err

    def collect_request_bool(self, form, key):
        err = self.collect_request_var(form, key)
        if err == '':
            if form[key] is None or form[key] == '':
                setattr(self, key, None)
            elif (form[key].lower() == 'true' or
                  form[key].lower == '1' or
                  form[key].lower() == 'yes' or
                  form[key] == 'on'):
                setattr(self, key, True)
            elif (form[key].lower() == 'false' or
                  form[key].lower == '0' or
                  form[key].lower() == 'no' or
                  form[key] == 'off'):
                setattr(self, key, False)
            else:
                raise ValueError('Invalid boolean value: {}'.format(form[key]))
        return err

    class Meta:
        database = db
