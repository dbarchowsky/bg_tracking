import unittest
from peewee import *
import bg_tracking
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


if __name__ == '__main__':
    unittest.main()
