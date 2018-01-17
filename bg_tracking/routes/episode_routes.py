from flask import Blueprint
from flask import render_template
from bg_tracking.models import *

episode_routes = Blueprint('episode_routes', __name__, template_folder='templates')


@episode_routes.route('/episodes/')
def listings():
    """List all episodes in database."""
    episodes = (
        Episode
        .select()
        .join(Show)
        .order_by(Show.name, Episode.number)
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
    e = Episode.get(Episode.id == episode_id)
    bgs = Background.select().where(Background.episode == episode_id).order_by(Background.scene)
    return render_template('episode_details.html', episode=e, bgs=bgs)


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
