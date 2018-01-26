from flask import request, Blueprint
from flask import render_template
from bg_tracking.models import *
from bg_tracking.forms import EpisodeForm
from bg_tracking.routes.episode_utils import EpisodeUtils

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


@episode_routes.route('/episode/<int:record_id>', defaults={'sort_criteria': 'scene',
                                                            'order': 'asc'
                                                            })
@episode_routes.route('/episode/<int:record_id>/sorted/by/<string:sort_criteria>',
                      defaults={'order': 'desc'})
@episode_routes.route('/episode/<int:record_id>/sorted/by/<string:sort_criteria>/<string:order>')
def details_view(record_id, sort_criteria, order):
    """
    List backgrounds in the requested episode.
    :param record_id: Id of the episode to display
    :type record_id: int
    :param sort_criteria: Criteria to use to display BG listings.
    :type sort_criteria: string
    :param order: Sort order, e.g. asc or desc
    :type sort_criteria: string
    :return: Response
    """
    return EpisodeUtils.render_details_view(record_id, sort_criteria, order)


@episode_routes.route('/episode/<int:record_id>/edit/')
@episode_routes.route('/episode/edit/', methods=['GET'], defaults={'record_id': None})
def edit_record(record_id):
    """
    Process form data & use it to create and update Episode records.
    :param record_id: Episode id in database.
    :type record_id: int
    :return: Response
    """
    if record_id:
        # editing existing record
        try:
            e = Episode.get(Episode.id == record_id)
        except Episode.DoesNotExist:
            err = 'The requested episode could not be found.'
            return render_template('error.html', error_msg=err)
    else:
        # editing new record
        e = Episode()
        if request.args.get('show_id'):
            # retrieve show details
            try:
                e.show = Show.get(Show.id == int(request.args.get('show_id')))
            except Show.DoesNotExist:
                err = 'The requested show could not be found.'
                return render_template('error.html', error_msg=err)
    form = EpisodeForm(obj=e)
    return render_template('episode_form.html', form=form, episode=e)


@episode_routes.route('/episode/commit/', methods=['POST'])
def save_edit():
    """
    Create new episode record.
    :return: Response
    """
    episode_id = request.form['id']
    if episode_id:
        try:
            e = Episode.get(id=episode_id)
        except Episode.DoesNotExist:
            return render_template('error.html', error_msg='The requested episode could not be retrieved.')
    else:
        e = Episode()

    status = {'success': None, 'error': None}
    form = EpisodeForm(request.form, obj=e)
    if form.validate():
        form.populate_obj(e)
        e.save()
        status['success'] = 'The changes have been saved.'
    else:
        status['error'] = 'There were problems saving the changes.'
        return render_template('episode_form.html', form=form, episode=e, status=status)

    return EpisodeUtils.render_details_view(e.id, 'scene', 'asc', status=status)
