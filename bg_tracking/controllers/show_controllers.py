from flask import Blueprint, flash, redirect, url_for, request
from flask import render_template
from peewee import *
from bg_tracking.models import *
from bg_tracking.utils import varunencode
from bg_tracking.controllers.utils import get_or_404
from bg_tracking.forms.forms import ShowForm

show_routes = Blueprint('show_routes', __name__, template_folder='templates')


@show_routes.route('/shows/')
def listings():
    shows = (Show
             .select(Show,
                     fn.COUNT(Episode.id).alias('episode_count')
                     )
             .join(Episode, JOIN.LEFT_OUTER)
             .order_by(Show.title, Show.season)
             .group_by(Show.id)
             )
    return render_template('show_list.html', title='Shows', shows=shows)


@show_routes.route('/show/<int:record_id>')
def details_view(record_id):
    """
    List the episodes available in the requested show.
    :param record_id: Show id matching database record.
    :type record_id: int
    :return: Response
    """
    s = get_or_404(Show.select().where(Show.id == record_id))
    try:
        episodes = get_episode_listings(s.id)
    except Episode.DoesNotExist:
        msg = 'Error retrieving episodes in {}'.format(s.title)
        return render_template('error.html', error_msg=msg)
    return render_template('show_details.html', title=str(s), show=s, episodes=episodes)


@show_routes.route('/show/<string:show_title>/season/<int:season>')
def details_by_title(show_title, season):
    """
    List the episodes available in the requested show.
    :param show_title: Show title
    :type show_title: str
    :param season: Season
    :type season: int
    :return: Response
    """
    show_title = varunencode(show_title)
    try:
        s = Show.get(Show.title == show_title, Show.season == season)
    except Show.DoesNotExist:
        msg = 'The show "{}" was not found.'.format(show_title)
        return render_template('error.html', error_msg=msg)
    else:
        try:
            episodes = get_episode_listings(s.id)
        except Episode.DoesNotExist:
            msg = 'Error retrieving episodes in {}'.format(s.title)
            return render_template('error.html', error_msg=msg)
    return render_template('show_details.html', title=str(s), show=s, episodes=episodes)


@show_routes.route('/show/add', methods=['GET', 'POST'])
def add_record():
    s = Show()

    if request.method == 'POST':
        form = ShowForm(request.form, obj=s)
        if form.validate():
            form.populate_obj(s)
            s.save()
            flash('Show “{}” was successfully saved.'.format(s.title), 'info')
            return redirect(url_for('show_routes.details_view', record_id=s.id))
    else:
        form = ShowForm(obj=s)

    title = 'Add New Show'
    return render_template('show_form.html', show=s, form=form, title=title, action=request.url_rule.rule)
        

@show_routes.route('/show/<int:record_id>/edit', methods=['GET', 'POST'])
def edit_record(record_id):
    """
    Validate and serialize show data.
    :param record_id: Id of show record to edit
    :return: Response
    """
    s = get_or_404(Show.select(), Show.id == record_id)

    if request.method == 'POST':
        form = ShowForm(request.form, obj=s)
        if form.validate():
            form.populate_obj(s)
            s.save()
            flash('Show “{}” was successfully updated.'.format(s.title), 'info')
            return redirect(url_for('show_routes.details_view', record_id=s.id))
    else:
        form = ShowForm(obj=s)

    action = '/show/{}/edit/'.format(s.id)
    title = 'Editing {}'.format(str(s))
    return render_template('show_form.html', show=s, form=form, title=title, action=action)
            

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
                    finished_sq.alias('finished_bgs'),
                    approved_sq.alias('approved_bgs'),
                    )
            .join(Background, JOIN.LEFT_OUTER)
            .where(Episode.show == show_id)
            .group_by(Episode.id)
            .order_by(Episode.number)
            )
