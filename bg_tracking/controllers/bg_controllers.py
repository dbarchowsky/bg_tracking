from flask import request, render_template, Blueprint
from peewee import *
from bg_tracking.models import *

bg_routes = Blueprint('bg_routes', __name__, template_folder='templates')


@bg_routes.route('/bgs', defaults={'sort_criteria': 'scene', 'order': 'asc'})
@bg_routes.route('/bgs/sorted/by/<string:sort_criteria>', defaults={'order': 'asc'})
@bg_routes.route('/bgs/sorted/by/<string:sort_criteria>/<string:order>')
def listings(sort_criteria, order):
    """
    Renders sorted BG listings page content.
    :param sort_criteria: Column used to sort listings.
    :param order: Direction of the sort, e.g. asc or desc
    :return: Response
    """
    try:
        oby = get_order_by_func(sort_criteria, order)
    except AttributeError:
        return render_template('error.html', error_msg='Invalid sort criteria.')

    try:
        if sort_criteria in ['scene']:
            bgs = get_sorted_bg_listings_data_by_episode(oby)
        else:
            bgs = get_sorted_bg_listings_data(oby)
    except Background.DoesNotExist:
        return render_template('error.html', error_msg='BGs could not be retrieved.')
    return render_listings(bgs)


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


@bg_routes.route('/bg/edit/', methods=['GET'], defaults={'record_id': None})
@bg_routes.route('/bg/<int:record_id>/edit/')
def edit_record(record_id):
    """
    Create new background record.
    :param record_id: Background id matching record in database.
    :type record_id: int
    :return: Response
    """
    if record_id:
        try:
            bg = Background.get(Background.id == record_id)
        except Background.DoesNotExist:
            return record_not_found_response('BG')
    else:
        bg = Background()
    if request.args.get('episode_id'):
        try:
            bg.episode = Episode.get(Episode.id == int(request.args.get('episode_id')))
        except Episode.DoesNotExist:
            return record_not_found_response('episode')
    if bg.id:
        title = 'Editing {} “{}” scene {}{}'.format(
            bg.episode.format_padded_number(),
            bg.episode.title,
            bg.format_padded_scene(),
            bg.scene_modifier if bg.scene_modifier else '',
        )
    else:
        title = 'Editing New BG'
    try:
        e = (Episode
             .select(Episode.id,
                     Episode.number,
                     Episode.title,
                     Show.title,
                     Show.season
                     )
             .join(Show)
             .order_by(Show.title, Show.season, Episode.number)
             )
    except Episode.DoesNotExist:
        return record_not_found_response('episodes')
    return render_template('bg_form.html', title=title, bg=bg, episodes=e)


@bg_routes.route('/bg/edit/', methods=['POST'])
def save_edit():
    """
    Create new episode record.
    :return: Response
    """
    if request.method == 'POST':
        bg = Background()
        title = 'Not implemented.'
        return render_template('bg_form.html', title=title, bg=bg)
    else:
        return render_template('error.html', error_msg='Bad request.')


def record_not_found_response(type_name):
    """
    Return standard error template with message.
    :param type_name: Name of the object that wasn't found.
    :return: Response
    """
    err = 'The requested {} could not be retrieved.'.format(type_name)
    return render_template('error.html', error_msg=err)


def get_sorted_bg_listings_data_by_episode(order_by_func):
    """
    Retrieves sorted data used to render BG listings, grouped by episode number.
    :param order_by_func: Pointer to function used to sort the results.
    :return: List of Background objects.
    """
    return (Background
            .select(Background,
                    Episode.id,
                    Episode.number,
                    Episode.title,
                    Show.code,
                    )
            .join(Episode)
            .join(Show)
            .order_by(Episode.number, order_by_func(), Background.scene_modifier)
            )


def get_sorted_bg_listings_data(order_by_func, episode_id=None):
    """
    Retrieves sorted data used to render BG listings.
    :param order_by_func: Pointer to function used to sort the results.
    :param episode_id: Optional episode id to use to filter records.
    :return: List of Background objects.
    """
    if episode_id:
        return (Background
                .select(Background,
                        Episode.id,
                        Episode.number,
                        Episode.title,
                        Show.code,
                        )
                .join(Episode)
                .join(Show)
                .where(Background.episode == episode_id)
                .order_by(order_by_func(), Background.scene_modifier)
                )
    else:
        return (Background
                .select(Background,
                        Episode.id,
                        Episode.number,
                        Episode.title,
                        Show.code,
                        )
                .join(Episode)
                .join(Show)
                .order_by(order_by_func(), Background.scene_modifier)
                )


def get_order_by_func(sort_criteria, order):
    attr = getattr(Background, sort_criteria)
    if order.lower() == 'desc':
        return attr.desc
    return attr.asc


def render_listings(bgs):
    """
    Load BG listings template.
    :param bgs: List of Background objects.
    :return: Response
    """
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