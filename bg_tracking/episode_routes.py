from flask import Blueprint
from flask import render_template
from bg_tracking.models import *

episode_routes = Blueprint('episode_routes', __name__, template_folder='templates')


@episode_routes.route('/episodes/')
def listings():
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
    :return:
    """
    e = Episode.get(Episode.id == episode_id)
    bgs = Background.select().where(Background.episode == episode_id).order_by(Background.scene)
    return render_template('episode_detail.html', episode=e, bgs=bgs)
