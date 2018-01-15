from peewee import *
import os

db = SqliteDatabase(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'bgs.db'), **{})


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    
    def collect_request_var(self, form, key):
        try:
            if len(form[key]) > 0:
                setattr(self, key, form[key])
        except KeyError:
            return 'Expected input is missing: {} \n'.format(key)
        return ''
    
    class Meta:
        database = db
