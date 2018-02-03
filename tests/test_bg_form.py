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


@implements_to_string
class Location(TestModel):
    id = AutoField()
    name = TextField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'location'


@implements_to_string
class Background(TestModel):
    id = AutoField()
    episode = ForeignKeyField(Episode, db_column='episode_id', field='id', backref='backgrounds')
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

    def __str__(self):
        return 'Sc {}'.format(self.format_padded_scene())

    class Meta:
        db_table = 'background'


BGForm = model_form(Background)


class BGFormTestCase(unittest.TestCase):
    def setUp(self):
        Background.drop_table(True)
        Location.drop_table(True)
        Episode.drop_table(True)
        Show.drop_table(True)

        Show.create_table()
        Episode.create_table()
        Location.create_table()
        Background.create_table()

        self.show_a = Show.create(id=1, title='aa', season=1, code='abc')
        self.show_b = Show.create(id=2, title='bb', season=1, code='bcd')

        self.episode_a1 = Episode.create(id=1, title='a1', number=1, show=self.show_a)
        self.episode_a2 = Episode.create(id=2, title='a2', number=2, show=self.show_a)
        self.episode_b1 = Episode.create(id=3, title='b1', number=1, show=self.show_b)

        self.location_int = Location.create(id=1, name='interior')
        self.location_ext = Location.create(id=2, name='exterior')

        self.bg_a1a = Background.create(id=1,
                                        episode = self.episode_a1,
                                        scene=12,
                                        scene_modifier=None,
                                        width=4500,
                                        height=2500,
                                        overlay_count=0,
                                        partial=0,
                                        establishing_shot=1,
                                        pull=0,
                                        card=None,
                                        location=self.location_int,
                                        hours=1.5,
                                        date_started='2018-02-03',
                                        date_finished=None,
                                        approved=0)

    def test_defaults(self):
        defaults = {'episode': {'default': self.episode_a2},
                    'scene': {'default': 'hello world'},
                    'scene_modifier': {'default': None},
                    'width': {'default': 5800},
                    'height': {'default': 3300},
                    'overlay_count': {'default': 2},
                    'partial': {'default': 0},
                    'establishing_shot': {'default': 0},
                    'pull': {'default': 1},
                    'card': {'default': 1},
                    'location': {'default': self.location_ext},
                    'hours': {'default': 2.5},
                    'date_started': {'default': '20148-02-01'},
                    'date_finished': {'default': ''},
                    'approved': {'default': 0},
                    }
        BGFormDef = model_form(Background, field_args=defaults)

        form = BGFormDef()
        self.assertEqual(form.data, {'episode': defaults['episode']['default'],
                                     'scene': defaults['scene']['default'],
                                     'scene_modifier': defaults['scene_modifier']['default'],
                                     'width': defaults['width']['default'],
                                     'height': defaults['height']['default'],
                                     'overlay_count': defaults['overlay_count']['default'],
                                     'partial': False,
                                     'establishing_shot': False,
                                     'pull': True,
                                     'card': True,
                                     'location': defaults['location']['default'],
                                     'hours': defaults['hours']['default'],
                                     'date_started': defaults['date_started']['default'],
                                     'date_finished': None,
                                     'approved': False,
                                     })

        form = BGFormDef(obj=self.bg_a1a)
        self.assertEqual(form.data, {'episode': self.bg_a1a.episode,
                                     'scene': self.bg_a1a.scene,
                                     'scene_modifier': self.bg_a1a.scene_modifier,
                                     'width': self.bg_a1a.width,
                                     'height': self.bg_a1a.height,
                                     'overlay_count': self.bg_a1a.overlay_count,
                                     'partial': False,
                                     'establishing_shot': True,
                                     'pull': False,
                                     'card': False,
                                     'location': self.bg_a1a.location,
                                     'hours': self.bg_a1a.hours,
                                     'date_started': self.bg_a1a.date_started,
                                     'date_finished': self.bg_a1a.date_finished,
                                     'approved': False,
                                     })

    def test_bg_form(self):
        form = BGForm()
        self.assertEqual(sorted(form._fields.keys()), ['approved',
                                                       'card',
                                                       'date_finished',
                                                       'date_started',
                                                       'episode',
                                                       'establishing_shot',
                                                       'height',
                                                       'hours',
                                                       'location',
                                                       'overlay_count',
                                                       'partial',
                                                       'pull',
                                                       'scene',
                                                       'scene_modifier',
                                                       'width',
                                                       ])

        self.assertIsInstance(form.episode, ModelSelectField)
        self.assertIsInstance(form.scene, wtfields.IntegerField)
        self.assertIsInstance(form.scene_modifier, wtfields.TextField)
        self.assertIsInstance(form.width, wtfields.IntegerField)
        self.assertIsInstance(form.height, wtfields.IntegerField)
        self.assertIsInstance(form.overlay_count, wtfields.IntegerField)
        self.assertIsInstance(form.partial, wtfields.BooleanField)
        self.assertIsInstance(form.establishing_shot, wtfields.BooleanField)
        self.assertIsInstance(form.pull, wtfields.BooleanField)
        self.assertIsInstance(form.card, wtfields.BooleanField)
        self.assertIsInstance(form.location, ModelSelectField)
        self.assertIsInstance(form.hours, wtfields.FloatField)
        self.assertIsInstance(form.date_started, wtfields.DateField)
        self.assertIsInstance(form.date_finished, wtfields.DateField)
        self.assertIsInstance(form.card, wtfields.BooleanField)

        self.assertEqual(form.episode.label.text, 'Episode')
        self.assertEqual(form.scene.label.text, 'Scene')
        self.assertEqual(form.scene_modifier.label.text, 'Scene Modifier')

        # check that foreign key defaults to none
        self.assertIsNone(form.episode.data)
        self.assertIsNone(form.location.data)

        # check that the options look right
        self.assertEqual(list(form.episode.iter_choices()), [(self.episode_a1._pk, u'001 a1', False),
                                                             (self.episode_a2._pk, u'002 a2', False),
                                                             (self.episode_b1._pk, u'001 b1', False),
                                                             ])
