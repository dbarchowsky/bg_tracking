from flask import Blueprint, request
from flask import render_template
from peewee import *
from bg_tracking.models import *
from bg_tracking.utils import varunencode

show_routes = Blueprint('show_routes', __name__, template_folder='templates')


@show_routes.route('/shows/')
def listings():
    shows = Show.select().order_by(Show.title).order_by(Show.title, Show.season)
    return render_template('show_list.html', title='Shows', shows=shows)


@show_routes.route('/show/<int:record_id>')
def details_view(record_id):
    """
    List the episodes available in the requested show.
    :param record_id: Show id matching database record.
    :type record_id: int
    :return: Response
    """
    try:
        s = Show.get(Show.id == record_id)
    except Show.DoesNotExist:
        msg = 'The requested show was not found.'
        return render_template('error.html', error_msg=msg)
    else:
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


@show_routes.route('/show/edit')
def new_record_form():
    """Edit new show."""
    title = 'New Show'
    s = Show()
    return render_template('show_form.html', title=title, show=s)


@show_routes.route('/show/<int:record_id>/edit')
def edit_record_form(record_id):
    """
    Edit existing show records.
    """
    try:
        s = Show.get(Show.id == record_id)
    except Show.DoesNotExist:
        msg = 'The requested show was not found. '
        return render_template('error.html', error_msg=msg)
    else:
        title = 'Editing {} season {}'.format(s.title, s.season)
    return render_template('show_form.html', title=title, show=s)


@show_routes.route('/show/edit', methods=['POST', 'GET'])
def save_edit():
    """
    Validate and serialize show data.
    :return: Response
    """
    if request.method == 'POST':

        s = Show()
        try:
            s.collect_form_data(request.form)
        except ValueError as e:
            return render_template('error.html', show=s, error_msg=e)

        try:
            s.validate_form_data()
        except ValueError as e:
            return render_template('error.html', error_msg=e)

        s.save()

        # display record details
        title = '{} season {}'.format(s.title, s.season)
        status = 'The changes were successfully saved.'
        try:
            episodes = get_episode_listings(s.id)
        except Episode.DoesNotExist:
            msg = 'Error retrieving episodes in {}'.format(s.title)
            return render_template('error.html', error_msg=msg)
        return render_template('show_details.html', title=title, status=status, episodes=episodes, show=s)
    else:
        return render_template('error.html', error_msg='Bad request.')


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
                    fn.COUNT(Episode.id).alias('bg_count'),
                    finished_sq.alias('finished_bgs'),
                    approved_sq.alias('approved_bgs'),
                    )
            .join(Background)
            .where(Episode.show == show_id)
            .group_by(Episode.id)
            .order_by(Episode.number)
            )
