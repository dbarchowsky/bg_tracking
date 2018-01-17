from flask import Flask, request, session, abort, redirect
import os
import string
import random
from urllib import parse
from markupsafe import Markup
from bg_tracking.models import *
from bg_tracking.routes import *

app = Flask(__name__)
app.register_blueprint(show_routes)
app.register_blueprint(episode_routes)
app.register_blueprint(bg_routes)


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
    """
    Site landing page.
    :return: Response
    """
    return redirect('/bgs')


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
