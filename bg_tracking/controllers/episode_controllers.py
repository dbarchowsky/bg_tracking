from flask import render_template, request, redirect, url_for, abort, flash, Blueprint
from bg_tracking.models import *
from bg_tracking.forms import EpisodeForm
from bg_tracking.controllers.episode_utils import EpisodeUtils
from bg_tracking.controllers.utils import get_or_404, redirect_back, get_redirect_target

episode_routes = Blueprint('episode_routes', __name__, template_folder='templates')


@episode_routes.route('/episodes/')
def listings():
    """List all episodes in database."""
    episodes = (Episode
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


@episode_routes.route('/episode/add/', methods=['GET', 'POST'])
def add_record():
    """
    Process form data & use it to create and update Episode records.
    :return: Response
    """
    e = Episode()
    e.show = Show()

    if request.method == 'POST':
        form = EpisodeForm(request.form, obj=e)
        if form.validate():
            form.populate_obj(e)
            e.save()
            flash('Episode “{}” was successfully saved.'.format(e.title), 'info')
            return redirect(url_for('episode_routes.details_view', record_id=e.id))
    else:
        # load show if specified
        if request.args.get('show_id'):
            e.show = get_or_404(Show.select(), Show.id == int(request.args.get('show_id')))
        form = EpisodeForm(obj=e)

    title = 'Add New Episode'
    return render_template('episode_form.html', episode=e, form=form, title=title, action=request.url_rule.rule)


@episode_routes.route('/episode/<int:record_id>/edit/', methods=['GET', 'POST'])
def edit_record(record_id):
    """
    Create new episode record.
    :param record_id: Episode id in database.
    :type record_id: int
    :return: Response
    """
    e = get_or_404(Episode.select(), Episode.id == record_id)

    if request.method == 'POST':
        form = EpisodeForm(request.form, obj=e)
        if form.validate():
            form.populate_obj(e)
            e.save()
            flash('Episode “{}” was successfully updated.'.format(e.title), 'info')
            return redirect(url_for('episode_routes.details_view', record_id=e.id))
    else:
        form = EpisodeForm(obj=e)

    action = '/episode/{}/edit/'.format(e.id)
    title = 'Editing {}'.format(str(e))
    return render_template('episode_form.html', episode=e, form=form, title=title, action=action)
    

@episode_routes.route('/episode/<int:record_id>/delete/', methods=['GET', 'POST'])
def delete(record_id):
    """
    Display confirmation form before deleting Episode record.
    :param record_id: Id of Episode record to delete.
    :return: HTML Response
    """
    e = get_or_404(Episode.select(), Episode.id == record_id)

    if request.method == 'POST':
        episode_title = str(e)
        cnt = 0
        bgs = Background.select().where(Episode == e.id)
        for bg in bgs:
            bg.delete_instance()
            cnt = cnt + 1
        e.delete_instance()
        flash('Episode {} was successfully deleted along with {} BG{}.'.format(episode_title,
                                                                               cnt,
                                                                               '' if cnt == 1 else 's'))
        return redirect_back('episode_routes.listings')
    else:
        title = 'Deleting {}'.format(str(e))
        ref = get_redirect_target()

    return render_template('episode_confirm_delete.html', episode=e, title=title, next=ref)

