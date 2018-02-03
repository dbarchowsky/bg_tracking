import unittest
from peewee import *
from wtforms import fields as wtfields
from wtfpeewee.orm import model_form
from wtfpeewee.fields import *
from wtfpeewee._compat import PY2


if not PY2:
    implements_to_string = lambda x: x
else:
    def implements_to_string(cls):
        cls.__unicode__ = cls.__str__
        cls.__str__ = lambda x: x.__unicode__().encode('utf-8')
        return cls


test_db = SqliteDatabase(':memory:')


class TestModel(Model):
    class Meta:
        database = test_db


@implements_to_string
class Show(TestModel):
    id = AutoField()
    code = TextField(null=True)
    title = TextField()
    season = IntegerField()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'show'


@implements_to_string
class Episode(TestModel):
    id = AutoField()
    title = CharField()
    number = IntegerField()
    show = ForeignKeyField(Show, db_column='show_id', to_field='id', backref='episodes')

    def format_padded_number(self):
        return '%03d' % self.number

    def __str__(self):
        return "{} {}".format(self.format_padded_number(), self.title)

    class Meta:
        db_table = 'episode'


EpisodeForm = model_form(Episode)


class EpisodeFormTestCase(unittest.TestCase):
    def setUp(self):
        Episode.drop_table(True)
        Show.drop_table(True)

        Show.create_table()
        Episode.create_table()

        self.show_a = Show.create(id=1, title='aa', season=1, code='abc')
        self.show_b = Show.create(id=2, title='bb', season=1, code='bcd')

        self.episode_a1 = Episode.create(id=1, title='a1', number=1, show=self.show_a)
        self.episode_a2 = Episode.create(id=2, title='a2', number=2, show=self.show_a)
        self.episode_b1 = Episode.create(id=3, title='b1', number=1, show=self.show_b)

    def test_defaults(self):
        defaults = {'title': {'default': 'hello world'},
                    'number': {'default': 1},
                    'show': {'default': None},
                    }
        EpisodeFormDef = model_form(Episode, field_args=defaults)

        form = EpisodeFormDef()
        self.assertEqual(form.data, {'title': defaults['title']['default'],
                                     'number': defaults['number']['default'],
                                     'show': defaults['show']['default']})

        form = EpisodeFormDef(obj=self.episode_a1)
        self.assertEqual(form.data, {'title': self.episode_a1.title,
                                     'number': self.episode_a1.number,
                                     'show': self.episode_a1.show})

    def test_episode_form(self):
        form = EpisodeForm()
        self.assertEqual(sorted(form._fields.keys()), ['number', 'show', 'title'])

        self.assertIsInstance(form.title, wtfields.TextField)
        self.assertIsInstance(form.number, wtfields.IntegerField)
        self.assertIsInstance(form.show, ModelSelectField)

        self.assertEqual(form.title.label.text, 'Title')
        self.assertEqual(form.number.label.text, 'Number')
        self.assertEqual(form.show.label.text, 'Show')

        # check that foreign key defaults to none
        self.assertIsNone(form.show.data)

        # check that the options look right
        self.assertEqual(list(form.show.iter_choices()), [(self.show_a._pk, u'aa', False),
                                                          (self.show_b._pk, u'bb', False),
                                                          ])
