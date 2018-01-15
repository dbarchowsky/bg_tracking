from flask import Flask, request, session, abort
from flask import render_template
import os
import string
import random
from urllib import parse
from markupsafe import Markup
from bg_tracking import *
app = Flask(__name__)


def varunencode(s):
    s = s.replace('_', ' ')
    return parse.unquote(s)


@app.before_request
def before_request():
    # database connection
    base_model.db.connect()

    # CSRF token
    if request.method == "POST":
        token = session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(403)


@app.after_request
def after_request(response):
    base_model.db.close()
    return response


@app.route('/')
def landing():
    bgs = (
        Background
        .select()
        .join(Episode)
        .order_by(Episode.number, Background.scene)
        )
    return render_template('backgrounds.html', bgs=bgs)    
    
    
@app.route('/shows/')
def show_list():
    shows = Show.select().order_by(Show.name).order_by(Show.name, Show.season)
    return render_template('show_list.html', title='Shows', shows=shows)


@app.route('/show/edit')
def new_show_form():
    """Edit new show."""
    title = 'New Show'
    s = Show()
    return render_template('show_form.html', title=title, show=s)


@app.route('/show/<int:show_id>/edit')
def existing_show_form(show_id):
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


@app.route('/show/edit', methods=['POST', 'GET'])
def edit_show():
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


@app.route('/show/<string:show_title>')
def show_detail_by_title(show_title):
    """
    List the episodes available in the requested show.
    :param show_title: Show name
    :type show_title: str
    :return: Response
    """
    show_title = varunencode(show_title)
    try:
        s = Show.get(Show.name == show_title)
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


@app.route('/show/<int:show_id>')
def show_detail_by_id(show_id):
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


@app.route('/episodes/')
def episode_list():
    episodes = (
        Episode
        .select()
        .join(Show)
        .order_by(Show.name, Episode.number)
        )
    return render_template('episode_list.html', title='Episodes', episodes=episodes)


@app.route('/episode/<int:episode_id>')
def episode_detail(episode_id):
    """
    List backgrounds in the requested episode.
    :param episode_id: Id of the episode to display
    :type episode_id: int
    :return:
    """
    e = Episode.get(Episode.id == episode_id)
    bgs = Background.select().where(Background.episode == episode_id).order_by(Background.scene)
    return render_template('episode_detail.html', episode=e, bgs=bgs)


@app.template_filter('varencode')
def varencode_filter(s):
    if type(s) == 'Markup':
        s = s.unescape()
    s = s.replace(' ', '_')
    s = s.encode('utf8')
    s = parse.quote_plus(s)
    return Markup(s)


def generate_random_string(size=6, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = generate_random_string(12)
    return session['_csrf_token']


app.jinja_env.globals['csrf_token'] = generate_csrf_token

if not app.secret_key:
    app.secret_key = os.urandom(24)

# allow running from the command line
if __name__ == '__main__':
    # app.run(use_reloader=False, debug=True)  # pythonista environment
    app.run()
