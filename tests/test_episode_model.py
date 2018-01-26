import unittest

from peewee import *

from bg_tracking.models import *


class EpisodeTestCase(unittest.TestCase):
    """
    Tests Show-related page content.
    """
    def setUp(self):
        base_model.db.connect()

    def tearDown(self):
        base_model.db.close()

    def test_episode_details_query(self):

        episode_id = 1
        bg_count = 26
        show_title = 'Close Enough'
        season = 1

        # get most recent show
        e = (Episode
             .select(Episode,
                     fn.COUNT(Background.id).alias('bg_count'),
                     fn.SUM(Background.hours).alias('total_hours'),
                     fn.AVG(Background.hours).alias('avg_hours'))
             .join(Background, JOIN.LEFT_OUTER)
             .where(Episode.id == episode_id)
             .get()
             )

        self.assertEqual(e.id, episode_id)
        self.assertEqual(e.bg_count, bg_count)
        self.assertGreater(e.total_hours, 0)
        self.assertGreater(e.avg_hours, 0)
        self.assertEqual(e.show.title, show_title)
        self.assertEqual(e.show.season, season)

    def test_invalid_episode_id(self):

        episode_id = 999
        with self.assertRaises(Episode.DoesNotExist):
            Episode.get(Episode.id == episode_id)


if __name__ == '__main__':
    unittest.main()
