import unittest
from peewee import *

from bg_tracking.models import *


class EpisodeQueryTestCase(unittest.TestCase):
    """
    Tests Episode-related page content.
    """
    def setUp(self):
        base_model.db.connect()

    def tearDown(self):
        base_model.db.close()

    def test_bg_stats_query(self):

        # get BG statistics
        record_id = 3
        finished_alias = Episode.alias()
        finished_sq = (finished_alias
                       .select(fn.COUNT(finished_alias.id)).where((Background.date_finished.is_null(False)) &
                                                                  (Background.date_finished != ''))
                       .join(Background)
                       .where(finished_alias.id == Episode.id)
                       )
        approved_sq = (finished_alias
                       .select(fn.COUNT(finished_alias.id)).where(Background.approved == 1)
                       .join(Background)
                       .where(finished_alias.id == Episode.id)
                       )
        e = (Episode
             .select(Episode,
                     fn.COUNT(Background.id).alias('bg_count'),
                     fn.SUM(Background.hours).alias('total_hours'),
                     fn.AVG(Background.hours).alias('avg_hours'),
                     finished_sq.alias('finished_bgs'),
                     approved_sq.alias('approved_bgs'),
                     )
             .join(Background)
             .where(Episode.id == record_id)
             .get()
             )
        finished = (Background
                    .select(fn.COUNT(Background.id).alias('count'))
                    .where((Background.episode == record_id) &
                           (Background.date_finished.is_null(False)) &
                           (Background.date_finished != '')
                           )
                    .get()
                    )
        approved = (Background
                    .select(fn.COUNT(Background.id).alias('count'))
                    .where((Background.episode == record_id) &
                           (Background.approved == 1)
                           )
                    .get()
                    )
        self.assertGreaterEqual(e.bg_count, 22)
        self.assertGreaterEqual(e.total_hours, 34)
        self.assertGreaterEqual(e.finished_bgs, 8)
        self.assertGreaterEqual(e.approved_bgs, 0)
        self.assertGreaterEqual(finished.count, 8)
        self.assertGreaterEqual(approved.count, 0)


if __name__ == '__main__':
    unittest.main()
