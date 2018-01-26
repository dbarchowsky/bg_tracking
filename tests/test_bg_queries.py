import unittest

from peewee import *

from bg_tracking.models import *


class BgQueryTestCase(unittest.TestCase):
    """
    Tests BG-related page content.
    """
    def setUp(self):
        base_model.db.connect()

    def tearDown(self):
        base_model.db.close()

    def test_bg_stats_query(self):

        # get BG statistics
        s = (Background
             .select(fn.COUNT(Background.id).alias('count'),
                     fn.SUM(Background.hours).alias('total_hours'),
                     fn.AVG(Background.hours).alias('avg_hours'),
                     )
             .get()
             )

        self.assertGreater(s.count, 40)
        self.assertGreater(s.total_hours, 0)
        self.assertGreater(s.avg_hours, 0)

    def test_format_scene(self):
        s = Background()
        s.scene = 1
        self.assertEqual(s.format_padded_scene(), '001')
        s.scene = 10
        self.assertEqual(s.format_padded_scene(), '010')
        s.scene = 100
        self.assertEqual(s.format_padded_scene(), '100')
        s.scene = 1000
        self.assertEqual(s.format_padded_scene(), '1000')
        s.scene = 2
        s.scene_modifier = 'a'
        self.assertEqual(s.format_padded_scene(), '002a')


if __name__ == '__main__':
    unittest.main()
