from flask import Flask, request, session, abort
from flask import render_template
import os
import string
import random
from urllib import parse
from markupsafe import Markup
from bg_tracking.models import *
from bg_tracking.show_routes import show_routes

app = Flask(__name__)
app.register_blueprint(show_routes)


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
