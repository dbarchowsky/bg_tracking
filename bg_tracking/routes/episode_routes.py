from flask import Blueprint
from flask import render_template
from peewee import *
from bg_tracking.models import *

episode_routes = Blueprint('episode_routes', __name__, template_folder='templates')


@episode_routes.route('/episodes/')
def listings():
    """List all episodes in database."""
    episodes = (
        Episode
        .select()
        .join(Show)
        .order_by(Show.title, Episode.number)
        )
    return render_template('episode_list.html', title='Episodes', episodes=episodes)


@episode_routes.route('/episode/<int:episode_id>')
def details_view(episode_id):
    """
    List backgrounds in the requested episode.
    :param episode_id: Id of the episode to display
    :type episode_id: int
    :return: Response
    """
    try:
        e = (Episode
             .select(Episode,
                     fn.COUNT(Background.id).alias('bg_count'),
                     fn.SUM(Background.hours).alias('total_hours'),
                     fn.AVG(Background.hours).alias('avg_hours'))
             .join(Background, JOIN.LEFT_OUTER)
             .where(Episode.id == episode_id)
             .get()
             )
    except Episode.DoesNotExist:
        return render_template('error.html', error_msg='The requested episode was not found.')
    else:
        try:
            bgs = (Background
                   .select()
                   .where(Background.episode == episode_id)
                   .order_by(Background.scene)
                   )
        except Background.DoesNotExist:
            err = 'Error retrieving BGs for episode “{}”.'.format(e.title)
            return render_template('error.html', error_msg=err)
        stats = {
                'count': '{} BG{}'.format(e.bg_count, '' if e.bg_count == 1 else 's'),
                'total_hours': '{:.2f} total hour{}'.format(e.total_hours, '' if e.total_hours == 1 else 's'),
                'avg_hours': '{:.2f} hour{} per BG'.format(e.avg_hours, '' if e.total_hours == 1 else 's'),
                }
    return render_template('episode_details.html', episode=e, bgs=bgs, stats=stats)


@episode_routes.route('/episode/<int:episode_id>/edit/')
def edit_record_form(episode_id):
    """
    Edit existing episode record.
    :param episode_id: Episode id in database.
    :type episode_id: int
    :return: Response
    """
    return render_template('error.html', error_msg='Not implemented.')


@episode_routes.route('/episode/edit/')
def new_record_form():
    """
    Create new episode record.
    :return: Response
    """
    return render_template('error.html', error_msg='Not implemented.')
