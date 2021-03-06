from flask import render_template, request, flash, Blueprint
from peewee import fn, JOIN
from bg_tracking.models import *
from bg_tracking.forms import EpisodeForm
from bg_tracking.controllers.episode_utils import EpisodeUtils
from bg_tracking.controllers.utils import get_or_404, redirect_back, get_redirect_target

episode_routes = Blueprint('episode_routes', __name__, template_folder='templates')


@episode_routes.route('/episodes/')
def listings():
    """List all episodes in database."""
    finished_sq = (Background
                   .select(fn.COUNT(Background.id))
                   .where((Background.episode == Episode.id) &
                          (Background.date_finished.is_null(False)) &
                          (Background.date_finished != '')
                          )
                   )
    approved_sq = (Background
                   .select(fn.COUNT(Background.id))
                   .where((Background.episode == Episode.id) & (Background.approved == 1))
                   )
    episodes = (Episode
                .select(Episode,
                        Show,
                        fn.COUNT(Background.id).alias('bg_count'),
                        finished_sq.alias('finished_bgs'),
                        approved_sq.alias('approved_bgs'),
                        )
                .join(Show)
                .switch(Episode)
                .join(Background, JOIN.LEFT_OUTER)
                .group_by(Episode.id)
                .order_by(Show.title, Show.season, Episode.number)
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
            return redirect_back('episode_routes.details_view', record_id=e.id)
    else:
        # load show if specified
        if request.args.get('show_id'):
            e.show = get_or_404(Show.select(), Show.id == int(request.args.get('show_id')))
        form = EpisodeForm(obj=e)

    title = 'Add New Episode'
    ref = get_redirect_target()
    return render_template('episode_form.html',
                           episode=e,
                           form=form,
                           title=title,
                           next=ref,
                           action=request.url_rule.rule
                           )


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
            return redirect_back('episode_routes.details_view', record_id=e.id)
    else:
        form = EpisodeForm(obj=e)

    action = '/episode/{}/edit/'.format(e.id)
    title = 'Editing {}'.format(str(e))
    ref = get_redirect_target()
    return render_template('episode_form.html', episode=e, form=form, title=title, next=ref, action=action)
    

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
        e.delete_instance()
        flash('Episode {} was successfully deleted.'.format(episode_title), 'info')
        return redirect_back('episode_routes.listings')
    else:
        title = 'Deleting {}'.format(str(e))
        ref = get_redirect_target()

    return render_template('episode_confirm_delete.html', episode=e, title=title, next=ref)
