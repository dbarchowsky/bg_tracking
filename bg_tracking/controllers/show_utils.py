import re
from flask import request, url_for, redirect
from peewee import fn, JOIN
from bg_tracking.utils import varencode
from bg_tracking.controllers.utils import is_safe_url
from bg_tracking.models import Episode, Background


def redirect_back(show, endpoint, **kwargs):
    target = request.form['next']
    if target:
        # update the show title and season in case they have changed after an edit
        target = re.sub(r'/show/.*/season/.*$',
                        r'/show/{}/season/{}'.format(varencode(show.title), show.season),
                        target)
    if not target or not is_safe_url(target):
        target = url_for(endpoint, **kwargs)
    return redirect(target)


def get_episode_listings(show_id):
    """
    Get Episode listings for a given show.
    :param show_id: Show id
    :return: list of Episode objects
    """
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
    return (Episode
            .select(Episode.id,
                    Episode.number,
                    Episode.title,
                    fn.COUNT(Background.id).alias('bg_count'),
                    fn.SUM(Background.hours).alias('hours'),
                    finished_sq.alias('finished_bgs'),
                    approved_sq.alias('approved_bgs'),
                    )
            .join(Background, JOIN.LEFT_OUTER)
            .where(Episode.show == show_id)
            .group_by(Episode.id)
            .order_by(Episode.number)
            )
