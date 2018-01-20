import unittest
from peewee import *
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


if __name__ == '__main__':
    unittest.main()
