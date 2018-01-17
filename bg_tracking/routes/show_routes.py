from flask import Blueprint, request
from flask import render_template
from bg_tracking.models import *
from bg_tracking.utils import varunencode

show_routes = Blueprint('show_routes', __name__, template_folder='templates')


@show_routes.route('/shows/')
def listings():
    shows = Show.select().order_by(Show.name).order_by(Show.name, Show.season)
    return render_template('show_list.html', title='Shows', shows=shows)


@show_routes.route('/show/edit')
def new_record_form():
    """Edit new show."""
    title = 'New Show'
    s = Show()
    return render_template('show_form.html', title=title, show=s)


@show_routes.route('/show/<int:show_id>/edit')
def edit_record_form(show_id):
    """
    Edit existing show records.
    """
    try:
        s = Show.get(Show.id == show_id)
    except Show.DoesNotExist:
        msg = 'The requested show was not found. '
        return render_template('error.html', error_msg=msg)
    else:
        title = 'Editing {} season {}'.format(s.name, s.season)
    return render_template('show_form.html', title=title, show=s)


@show_routes.route('/show/edit', methods=['POST', 'GET'])
def save_edit():
    """Validate and serialize show data."""
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
        title = '{} season {}'.format(s.name, s.season)
        status = 'The changes were successfully saved.'
        try:
            episodes = Episode.select().where(Episode.show == s.id)
        except Episode.DoesNotExist:
            msg = 'Error retrieving episodes in {}'.format(s.name)
            return render_template('error.html', error_msg=msg)
        return render_template('show_detail.html', title=title, status=status, episodes=episodes, show=s)
    else:
        return render_template('error.html', error_msg='Bad request.')


@show_routes.route('/show/<int:show_id>')
def details_view(show_id):
    """
    List the episodes available in the requested show.
    :param show_id: Show name
    :type show_id: int
    :return: Response
    """
    try:
        s = Show.get(Show.id == show_id)
    except Show.DoesNotExist:
        msg = 'The requested show was not found.'
        return render_template('error.html', error_msg=msg)
    else:
        title = "{} season {}".format(s.name, s.season)
        try:
            episodes = Episode.select().where(Episode.show == s.id)
        except Episode.DoesNotExist:
            msg = 'Error retrieving episodes in {}'.format(s.name)
            return render_template('error.html', error_msg=msg)
    return render_template('show_detail.html', title=title, show=s, episodes=episodes)


@show_routes.route('/show/<string:show_title>/season/<int:season>')
def details_by_title(show_title, season):
    """
    List the episodes available in the requested show.
    :param show_title: Show name
    :type show_title: str
    :param season: Season
    :type season: int
    :return: Response
    """
    show_title = varunencode(show_title)
    try:
        s = Show.get(Show.name == show_title, Show.season == season)
    except Show.DoesNotExist:
        msg = 'The show "{}" was not found.'.format(show_title)
        return render_template('error.html', error_msg=msg)
    else:
        title = "{} season {}".format(s.name, s.season)
        try:
            episodes = Episode.select().where(Episode.show == s.id)
        except Episode.DoesNotExist:
            msg = 'Error retrieving episodes in {}'.format(s.name)
            return render_template('error.html', error_msg=msg)
    return render_template('show_detail.html', title=title, show=s, episodes=episodes)

