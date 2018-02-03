from flask import render_template
from peewee import *
from bg_tracking.models import *


class BGUtils:
    @staticmethod
    def record_not_found_response(type_name):
        """
        Return standard error template with message.
        :param type_name: Name of the object that wasn't found.
        :return: Response
        """
        err = 'The requested {} could not be retrieved.'.format(type_name)
        return render_template('error.html', error_msg=err)

    @staticmethod
    def get_sorted_bg_listings_data_by_episode(order_by_func):
        """
        Retrieves sorted data used to render BG listings, grouped by episode number.
        :param order_by_func: Pointer to function used to sort the results.
        :return: List of Background objects.
        """
        return (Background
                .select(Background,
                        Episode.id,
                        Episode.number,
                        Episode.title,
                        Show.code,
                        )
                .join(Episode)
                .join(Show)
                .order_by(Episode.number, order_by_func(), Background.scene_modifier)
                )

    @staticmethod
    def get_sorted_bg_listings_data(order_by_func, episode_id=None):
        """
        Retrieves sorted data used to render BG listings.
        :param order_by_func: Pointer to function used to sort the results.
        :param episode_id: Optional episode id to use to filter records.
        :return: List of Background objects.
        """
        if episode_id:
            return (Background
                    .select(Background,
                            Episode.id,
                            Episode.number,
                            Episode.title,
                            Show.code,
                            )
                    .join(Episode)
                    .join(Show)
                    .where(Background.episode == episode_id)
                    .order_by(order_by_func(), Background.scene_modifier)
                    )
        else:
            return (Background
                    .select(Background,
                            Episode.id,
                            Episode.number,
                            Episode.title,
                            Show.code,
                            )
                    .join(Episode)
                    .join(Show)
                    .order_by(order_by_func(), Background.scene_modifier)
                    )

    @staticmethod
    def get_order_by_func(sort_criteria, order):
        attr = getattr(Background, sort_criteria)
        if order.lower() == 'desc':
            return attr.desc
        return attr.asc

    @staticmethod
    def render_listings(bgs):
        """
        Load BG listings template.
        :param bgs: List of Background objects.
        :return: Response
        """
        s = (Background
             .select(fn.COUNT(Background.id).alias('count'),
                     fn.SUM(Background.hours).alias('total_hours'),
                     fn.AVG(Background.hours).alias('avg_hours'),
                     )
             .get()
             )
        count = '{} BG{}'.format(s.count, '' if s.count == 1 else 's')
        total = '{:.2f} total hour{}'.format(s.total_hours, '' if s.total_hours == 1 else 's')
        if s.avg_hours:
            avg = '{:.2f} hour{} per BG'.format(s.avg_hours, '' if s.avg_hours == 1 else 's')
        else:
            avg = None
        stats = {'count': count,
                 'total_hours': total,
                 'avg_hours': avg,
                 }
        return render_template('bg_list.html', title='BGs', bgs=bgs, stats=stats)
