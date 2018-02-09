from flask import request, render_template, flash, Blueprint
from bg_tracking.models import *
from bg_tracking.forms.forms import BGForm
from bg_tracking.controllers.bg_utils import BGUtils
from bg_tracking.controllers.utils import get_or_404, redirect_back, get_redirect_target

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
        oby = BGUtils.get_order_by_func(sort_criteria, order)
    except AttributeError:
        return render_template('error.html', error_msg='Invalid sort criteria.')

    try:
        if sort_criteria in ['scene']:
            bgs = BGUtils.get_sorted_bg_listings_data_by_episode(oby)
        else:
            bgs = BGUtils.get_sorted_bg_listings_data(oby)
    except Background.DoesNotExist:
        return render_template('error.html', error_msg='BGs could not be retrieved.')
    return BGUtils.render_listings(bgs)


@bg_routes.route('/bg/<int:record_id>')
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


@bg_routes.route('/bg/add/', methods=['GET', 'POST'])
def add_record():
    """
    Process form data & use it to create and update Episode records.
    :return: Response
    """
    bg = Background()
    bg.episode = Episode()
    bg.location = Location()
    ref = ''

    if request.method == 'POST':
        form = BGForm(request.form, obj=bg)
        if form.validate():
            form.populate_obj(bg)
            bg.save()
            flash('Scene {} was successfully saved.'.format(bg.scene), 'info')
            return redirect_back('bg_routes.details_view', record_id=bg.id)
    else:
        # load show if specified
        if request.args.get('episode_id'):
            bg.episode = get_or_404(Episode.select(), Episode.id == int(request.args.get('episode_id')))
        ref = get_redirect_target()
        form = BGForm(obj=bg)

    title = 'Adding New BG'
    return render_template('bg_form.html', bg=bg, form=form, title=title, next=ref, action=request.url_rule.rule)


@bg_routes.route('/bg/<int:record_id>/edit/', methods=['GET', 'POST'])
def edit_record(record_id):
    """
    Create new background record.
    :param record_id: Background id matching record in database.
    :type record_id: int
    :return: Response
    """
    bg = get_or_404(Background.select(), Background.id == record_id)
    ref = ''

    if request.method == 'POST':
        form = BGForm(request.form, obj=bg)
        if form.validate():
            form.populate_obj(bg)
            bg.save()
            flash('Scene {} was successfully updated.'.format(bg.scene), 'info')
            return redirect_back('bg_routes.details_view', record_id=bg.id)
    else:
        form = BGForm(obj=bg)
        ref = get_redirect_target()

    action = '/bg/{}/edit/'.format(bg.id)
    title = 'Editing {} “{}” scene {}'.format(bg.episode.format_padded_number(),
                                              bg.episode.title,
                                              bg.format_padded_scene())
    return render_template('bg_form.html', bg=bg, form=form, title=title, action=action, next=ref)
    

@bg_routes.route('/bg/<int:record_id>/delete/', methods=['GET', 'POST'])
def delete(record_id):
    """
    Display confirmation form before deleting BG record.
    :param record_id: Id of BG record to delete.
    :return: HTML Response
    """
    bg = get_or_404(Background.select(), Background.id == record_id)

    if request.method == 'POST':
        bg_name = str(bg)
        bg.delete_instance()
        flash('{} BG was successfully deleted.'.format(bg_name), 'info')
        return redirect_back('bg_routes.listings')
    else:
        title = 'Deleting {}'.format(str(bg))
        ref = get_redirect_target()

    return render_template('bg_confirm_delete.html', bg=bg, title=title, next=ref)
