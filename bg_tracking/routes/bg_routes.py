from flask import Blueprint
from flask import render_template
from bg_tracking.models import *

bg_routes = Blueprint('bg_routes', __name__, template_folder='templates')


@bg_routes.route('/bgs')
def landing():
    bgs = (Background
           .select()
           .join(Episode)
           .order_by(Episode.number, Background.scene)
           )
    return render_template('bg_list.html', title='BGs', bgs=bgs)


@bg_routes.route('/bg/<record_id>')
def details_view(record_id):
    """
    Display details for single BG record.
    :param record_id: Background id matching record in database.
    :type record_id: int
    :return: Response
    """
    try:
        bg = Background.get(Background.id == record_id)
    except Background.DoesNotExist:
        err = "Background with id {} not found. ".format(record_id)
        return render_template('error.html', error_msg=err)
    else:
        title = 'Episode {} “{}” scene {}'.format(
            bg.episode.format_padded_number(),
            bg.episode.title,
            bg.format_padded_scene()
            )
    return render_template('bg_details.html', title=title, bg=bg)


@bg_routes.route('/bg/<record_id>/edit/')
def edit_record_form(record_id):
    """
    Edit existing background record.
    :param record_id: Background id matching record in database.
    :type record_id: int
    :return: Response
    """
    bg = Background.get(Background.id == record_id)
    return render_template('error.html', error_msg='Not implemented.', bg=bg)


@bg_routes.route('/bg/edit/')
def new_record_form():
    """
    Create new background record.
    :return: Response
    """
    return render_template('error.html', error_msg='Not implemented.')
