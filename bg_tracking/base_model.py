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

    def collect_request_int(self, form, key):
        err = self.collect_request_var(form, key)
        if len(err) > 0:
            return err
        v = getattr(self, key)
        if v:
            setattr(self, key, int(v))
        return ''

    def collect_request_string(self, form, key):
        return self.collect_request_var(form, key)

    class Meta:
        database = db
