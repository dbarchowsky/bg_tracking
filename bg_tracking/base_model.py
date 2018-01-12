from peewee import *
import os

db = SqliteDatabase(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'bgs.db'), **{})


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = db
