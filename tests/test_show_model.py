import unittest
from peewee import *
import time
from bg_tracking.models import *


class ShowModelTestCase(unittest.TestCase):
    """
    Tests Show-related page content.
    """
    def setUp(self):
        base_model.db.connect()

    def tearDown(self):
        base_model.db.close()

    def test_show_episodes_query(self):

        show_id = 1

        # get episode list
        e = (Episode
             .select(Episode.id,
                     Episode.number,
                     Episode.title,
                     fn.COUNT(Episode.id).alias('bg_count'),
                     )
             .join(Background)
             .where(Episode.show == show_id)
             .group_by(Episode.id)
             .order_by(Episode.number)
             )

        self.assertEqual(len(list(e)), 3)

        self.assertEqual(e[0].number, 8)
        self.assertEqual(e[0].bg_count, 1)

        self.assertEqual(e[1].number, 9)
        self.assertEqual(e[1].bg_count, 26)

        self.assertEqual(e[2].number, 10)
        self.assertEqual(e[2].bg_count, 15)

    def _test_collect_form_data(self, data):
        s = Show()
        s.collect_form_data(data)
        self.assertEqual(s.id, data['id'])
        self.assertEqual(s.title, data['title'])
        self.assertEqual(s.code, data['code'])
        self.assertEqual(s.season, data['season'])

    def test_collect_form_data(self):
        self._test_collect_form_data({
            'id': 2,
            'title': 'unit test',
            'code': time.strftime('%Y-%m-%d %M:%H'),
            'season': 1
            })

    def test_collect_form_data_with_no_id(self):
        self._test_collect_form_data({
            'id': None,
            'title': 'unit test',
            'code': time.strftime('%Y-%m-%d %M:%H'),
            'season': 1
        })

    def test_collect_form_data_empty(self):
        data = {
            'id': '',
            'title': '',
            'code': '',
            'season': ''
            }
        s = Show()
        s.collect_form_data(data)
        self.assertEqual(s.id, None)
        self.assertEqual(s.title, data['title'])
        self.assertEqual(s.code, data['code'])
        self.assertEqual(s.season, None)

    def test_collect_form_data_invalid_key(self):
        data = {
            'bogus': 'value',
            }
        s = Show()
        with self.assertRaises(KeyError) as e:
            s.collect_form_data(data)
        self.assertRegex(str(e.exception), 'Expected input is missing: id')

    def test_collect_form_data_none(self):
        data = {
            'id': None,
            'title': None,
            'code': None,
            'season': None
            }
        s = Show()
        s.collect_form_data(data)
        self.assertEqual(s.id, data['id'])
        self.assertEqual(s.title, '')
        self.assertEqual(s.code, '')
        self.assertEqual(s.season, data['season'])

    def test_validate_form_data(self):
        data = {
            'id': None,
            'title': 'unit test',
            'code': time.strftime('%Y-%m-%d %M:%H'),
            'season': 1
        }
        s = Show()
        s.collect_form_data(data)
        s.validate_form_data()
        self.assertEqual(s.title, data['title'])

    def test_validate_form_data_missing_title(self):
        data = {
            'id': None,
            'title': '',
            'code': time.strftime('%Y-%m-%d %M:%H'),
            'season': 1
        }
        s = Show()
        s.collect_form_data(data)
        with self.assertRaises(ValueError) as e:
            s.validate_form_data()
        self.assertRegex(str(e.exception), 'title is required')

    def test_validate_form_data_invalid_id(self):
        data = {
            'id': 'abc',
            'title': 'test',
            'code': time.strftime('%Y-%m-%d %M:%H'),
            'season': 1
        }
        s = Show()
        with self.assertRaises(ValueError) as e:
            s.collect_form_data(data)
        self.assertRegex(str(e.exception), 'Invalid value for id')

    def test_validate_form_data_missing_season(self):
        data = {
            'id': '',
            'title': 'test',
            'code': time.strftime('%Y-%m-%d %M:%H'),
            'season': None
        }
        s = Show()
        s.collect_form_data(data)
        with self.assertRaises(ValueError) as e:
            s.validate_form_data()
        self.assertRegex(str(e.exception), 'season is required')


if __name__ == '__main__':
    unittest.main()
