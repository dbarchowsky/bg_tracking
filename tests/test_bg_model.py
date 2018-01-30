import unittest
from bg_tracking.models import *
from peewee import *


class BgModelTestCase(unittest.TestCase):
    """
    Tests BG-related routines.
    """
    def setUp(self):
        base_model.db.connect()

    def tearDown(self):
        base_model.db.close()

    def test_integer_input_field(self):
        b = Background()
        self.assertNotIsInstance(b.scene_modifier, TextField)

    def test_bg_collect_form_data_number_values(self):
        b = Background()
        data = {'id': None,
                'episode': 4,
                'scene': 87,
                'scene_modifier': '',
                'width': 4500,
                'height': 2500,
                'overlay_count': '',
                'partial': '',
                'establishing_shot': '',
                'pull': '',
                'location': 1,
                'hours': '',
                'date_started': '',
                'date_finished': '',
                'approved': ''
                }
        b.collect_form_data(data)
        self.assertEqual(b.id, data['id'])
        self.assertIsInstance(b.episode, Episode)
        self.assertEqual(b.episode.id, data['episode'])
        self.assertEqual(b.scene, data['scene'])
        self.assertEqual(b.width, data['width'])
        self.assertEqual(b.height, data['height'])
        self.assertEqual(b.overlay_count, None)
        self.assertEqual(b.partial, None)
        self.assertEqual(b.establishing_shot, None)
        self.assertEqual(b.pull, None)
        self.assertIsInstance(b.location, Location)
        self.assertEqual(b.location.id, data['location'])
        self.assertEqual(b.establishing_shot, None)
        self.assertEqual(b.date_started, None)
        self.assertEqual(b.date_finished, None)
        self.assertEqual(b.approved, None)

    def test_bg_collect_form_data_string_values(self):
        b = Background()
        data = {'id': '',
                'episode': '4',
                'scene': '87',
                'scene_modifier': '',
                'width': '4500',
                'height': '2500',
                'overlay_count': '',
                'partial': '',
                'establishing_shot': '',
                'pull': '',
                'location': '1',
                'hours': '',
                'date_started': '',
                'date_finished': '',
                'approved': ''
                }
        b.collect_form_data(data)
        self.assertEqual(b.id, None)
        self.assertIsInstance(b.episode, Episode)
        self.assertEqual(b.episode.id, int(data['episode']))
        self.assertEqual(b.scene, int(data['scene']))
        self.assertEqual(b.width, int(data['width']))
        self.assertEqual(b.height, int(data['height']))
        self.assertEqual(b.overlay_count, None)
        self.assertEqual(b.partial, None)
        self.assertEqual(b.establishing_shot, None)
        self.assertEqual(b.pull, None)
        self.assertIsInstance(b.location, Location)
        self.assertEqual(b.location.id, int(data['location']))
        self.assertEqual(b.establishing_shot, None)
        self.assertEqual(b.date_started, None)
        self.assertEqual(b.date_finished, None)
        self.assertEqual(b.approved, None)

    def test_bg_collect_form_data(self):
        b = Background()
        data = {'id': '2',
                'episode': '4',
                'scene': '87',
                'scene_modifier': '',
                'width': '4500',
                'height': '2500',
                'overlay_count': '8',
                'partial': 'True',
                'establishing_shot': 'Yes',
                'pull': 'Off',
                'location': '1',
                'hours': '.75',
                'date_started': '1/28/2018',
                'date_finished': '2018-01-29',
                'approved': '1'
                }
        b.collect_form_data(data)
        self.assertEqual(b.id, int(data['id']))
        self.assertIsInstance(b.episode, Episode)
        self.assertEqual(b.episode.id, int(data['episode']))
        self.assertEqual(b.scene, int(data['scene']))
        self.assertEqual(b.width, int(data['width']))
        self.assertEqual(b.height, int(data['height']))
        self.assertEqual(b.overlay_count, int(data['overlay_count']))
        self.assertEqual(b.partial, True)
        self.assertEqual(b.establishing_shot, True)
        self.assertEqual(b.pull, False)
        self.assertIsInstance(b.location, Location)
        self.assertEqual(b.location.id, int(data['location']))
        self.assertEqual(b.hours, .75)
        self.assertEqual(b.date_started, '2018-01-28')
        self.assertEqual(b.date_finished, '2018-01-29')
        self.assertEqual(b.approved, True)

    def test_bg_get_by_id(self):
        record_id = 56
        bg = Background.get(Background.id == record_id)
        self.assertEqual(bg.card, 1)


if __name__ == '__main__':
    unittest.main()
