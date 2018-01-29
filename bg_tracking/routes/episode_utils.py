from flask import render_template
from peewee import *
from math import floor
from bg_tracking.models import *
from bg_tracking.routes.bg_routes import get_order_by_func, get_sorted_bg_listings_data


class EpisodeUtils:

    @staticmethod
    def render_details_view(record_id, sort_criteria, order, **kwargs):
        """
        List backgrounds in the requested episode.
        :param record_id: Id of the episode to display
        :type record_id: int
        :param sort_criteria: Criteria to use to display BG listings.
        :type sort_criteria: string
        :param order: Sort order, e.g. asc or desc
        :type order: string
        :param kwargs: extra arguments to pass to flask's render_template()
        :return: Response
        """
        try:
            e = (Episode
                 .select(Episode,
                         fn.COUNT(Background.id).alias('bg_count'),
                         fn.SUM(Background.hours).alias('total_hours'),
                         fn.AVG(Background.hours).alias('avg_hours'),
                         )
                 .join(Background, JOIN.LEFT_OUTER)
                 .where(Episode.id == record_id)
                 .get()
                 )
        except Episode.DoesNotExist:
            return render_template('error.html', error_msg='The requested episode was not found.')
        else:
            try:
                oby = get_order_by_func(sort_criteria, order)
            except AttributeError:
                return render_template('error.html', error_msg='Invalid sort criteria.')

            try:
                bgs = get_sorted_bg_listings_data(oby, episode_id=e.id)
            except Background.DoesNotExist:
                err = 'Error retrieving BGs for episode “{}”.'.format(e.title)
                return render_template('error.html', error_msg=err)

            finished_bgs = EpisodeUtils.get_finished_bg_count(e.id)
            approved_bgs = EpisodeUtils.get_approved_bg_count(e.id)

            if e.total_hours:
                total_hours = '{:.2f} total hour{}'.format(e.total_hours, '' if e.total_hours == 1 else 's')
            else:
                total_hours = '0 total hours'
            if e.avg_hours:
                avg_hours = '{:.2f} hour{} per BG'.format(e.avg_hours, '' if e.total_hours == 1 else 's')
            else:
                avg_hours = ''
            stats = {
                'count': '{} BG{}'.format(e.bg_count, '' if e.bg_count == 1 else 's'),
                'total_hours': total_hours,
                'avg_hours': avg_hours,
                'finished': '{} finished'.format(finished_bgs),
                'finished_pct': floor((finished_bgs/e.bg_count) * 10) * 10,
                'approved': '{} approved'.format(approved_bgs),
                'approved_pct': floor((approved_bgs/e.bg_count) * 10) * 10,
            }
        return render_template('episode_details.html', episode=e, bgs=bgs, stats=stats, **kwargs)

    @staticmethod
    def get_finished_bg_count(episode_id):

        try:
            finished = (Background
                        .select(fn.COUNT(Background.id).alias('count'))
                        .where((Background.episode == episode_id) &
                               (Background.date_finished.is_null(False)) &
                               (Background.date_finished != '')
                               )
                        .get()
                        )
        except Background.DoesNotExist:
            return render_template('error.html', error_msg='Error retrieving statistics for requested episode.')
        return finished.count

    @staticmethod
    def get_approved_bg_count(episode_id):
        try:
            approved = (Background
                        .select(fn.COUNT(Background.id).alias('count'))
                        .where((Background.episode == episode_id) &
                               (Background.approved == 1)
                               )
                        .get()
                        )
        except Background.DoesNotExist:
            return render_template('error.html', error_msg='Error retrieving statistics for requested episode.')
        return approved.count
