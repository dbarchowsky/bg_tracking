from flask import Blueprint
from flask import render_template
from bg_tracking.models import *

bg_routes = Blueprint('bg_routes', __name__, template_folder='templates')


@bg_routes.route('/bgs')
def landing():
    bgs = (
        Background
        .select()
        .join(Episode)
        .order_by(Episode.number, Background.scene)
        )
    return render_template('backgrounds.html', bgs=bgs)


@bg_routes.route('/bg/<int:bg_id>')
def bg_details(bg_id):
    """
    Display details for single BG record.
    :param bg_id: Background id matching record in database.
    :type bg_id: int
    :return: Response
    """
    try:
        bg = (Background
                .select(Background.id == bg_id)
                .join(Episode)
                .get()
                )
    except Background.DoesNotExist:
        err = "Background with id {} not found. ".format(bg_id)
        return render_template('error.html', error_msg=err)
    else:
        title = 'Episode {} “{}” scene {}'.format(
            bg.episode.format_padded_number(),
            bg.episode.name,
            bg.format_padded_scene()
            )
    return render_template('bg_details.html', title=title, bg=bg)


@bg_routes.route('/bg/<int:bg_id>/edit/')
def edit_record_form(bg_id):
    """
    Edit existing background record.
    :param bg_id: Background id matching record in database.
    :type bg_id: int
    :return: Response
    """
    return render_template('error.html', error_msg='Not implemented.')


@bg_routes.route('/bg/edit/')
def new_record_form():
    """
    Create new background record.
    :return: Response
    """
    return render_template('error.html', error_msg='Not implemented.')
