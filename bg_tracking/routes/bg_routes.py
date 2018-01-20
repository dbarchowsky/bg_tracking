from flask import Blueprint
from flask import render_template
from peewee import *
from bg_tracking.models import *

bg_routes = Blueprint('bg_routes', __name__, template_folder='templates')


@bg_routes.route('/bgs')
def listings():
    bgs = (Background
           .select()
           .join(Episode)
           .order_by(Episode.number, Background.scene)
           )
    s = (Background
         .select(fn.COUNT(Background.id).alias('count'),
                 fn.SUM(Background.hours).alias('total_hours'),
                 fn.AVG(Background.hours).alias('avg_hours'),
                 )
         .get()
         )
    count = '{} BG{}'.format(s.count, '' if s.count == 1 else 's')
    total = '{:.2f} total hour{}'.format(s.total_hours, '' if s.total_hours == 1 else 's')
    if s.avg_hours:
        avg = '{:.2f} hour{} per BG'.format(s.avg_hours, '' if s.avg_hours == 1 else 's')
    else:
        avg = None
    stats = {'count': count,
             'total_hours': total,
             'avg_hours': avg,
             }
    return render_template('bg_list.html', title='BGs', bgs=bgs, stats=stats)


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
