from flask import Flask, request, session
from flask import render_template
import os
import string
import random
import urllib
from markupsafe import Markup
from bg_tracking import *
app = Flask(__name__)


def varunencode(s):
    s = s.replace('_', ' ')
    return urllib.parse.unquote(s)


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
    bgs = (Background
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
    show = Show()
    return render_template('show_form.html', title=title, show=show)


@app.route('/show/<int:show_id>/edit')
def existing_show_form():
    """
    Edit existing show records.
    """
    try:
        show = Show.get(Show.id == show_id)
    except Show.DoesNotExist:
        msg = 'The requested show was not found. '
        return render_template('error.html', error_msg=msg)
    else:
        title = 'Editing {} season {}'.format(show.name, show.season)
    return render_template('show_form.html', title=title, show=show)


@app.route('/show/edit', methods=['POST', 'GET'])
def edit_show():
    """Validate and serialize show data."""
    error = None
    if request.method == 'POST':

        show = Show()
        try:
            show.collect_form_data(request.form)
        except ValueError as e: 
            return render_template('show_form.html', show=show, error_msg=error)
        try: 
            show.validate_form_data(request.form)
        except ValueError as e: 
            return render_template('show_form.html', title=title, show=show, error_msg=error)
                            
        # display record details
        title = "{} season {}".format(show.name, show.season)
        try:
            episodes = Episode.select().where(Episode.show == show.id)
        except:
            title = 'Error retrieving episodes in {}'.format(show.name)
        return render_template('show_detail.html', title=title, show=show)
    else:
        return render_template('error.html', error_msg='Bad request.')


@app.route('/show/<string:show_title>')
def show_detail_by_title(show_title):
    """
    List the episodes available in the requested show.
    :param show: Show name
    :return: Response
    """
    show_title = varunencode(show_title)
    try:
        show = Show.get(Show.name == show_title)
    except Show.DoesNotExist:
        msg = 'The show "{}" was not found.'.format(show_title)
        return render_template('error.html', error_msg=msg)
    else:
        title = "{} season {}".format(show.name, show.season)
        try:
            episodes = Episode.select().where(Episode.show == show.id)
        except:
            title = 'Error retrieving episodes in {}'.format(show.name)
    return render_template('show_detail.html', title=title, show=show, episodes=episodes)


@app.route('/show/<int:show_id>')
def show_detail_by_id(show_id):
    """
    List the episodes available in the requested show.
    :param show: Show name
    :return: Response
    """
    try:
        show = Show.get(Show.id == show_id)
    except Show.DoesNotExist:
        msg = 'The requested show was not found.'
        return render_template('error.html', error_msg=msg)
    else:
        title = "{} season {}".format(show.name, show.season)
        try:
            episodes = Episode.select().where(Episode.show == show.id)
        except:
            title = 'Error retrieving episodes in {}'.format(show.name)
    return render_template('show_detail.html', title=title, show=show, episodes=episodes)


@app.route('/episodes/')
def episode_list():
    episodes = (Episode
        .select()
        .join(Show)
        .order_by(Show.name, Episode.number)
        )
    return render_template('episode_list.html', title='Episodes', episodes=episodes)


@app.route('/episode/<int:episode_id>')
def episode_detail(episode_id):
    """
    List backgrounds in the requested episode.
    :param episode_id:
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
    s = urllib.parse.quote_plus(s)
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
    app.run(use_reloader=False, debug=True)
    # app.run()
