from flask import Flask, redirect
from flask_wtf.csrf import CSRFProtect
import os
from bg_tracking.models import *
from bg_tracking.controllers import *
from bg_tracking.controllers.utils import generate_csrf_token
from bg_tracking import jinja_filters

app = Flask(__name__)
app.register_blueprint(show_routes)
app.register_blueprint(episode_routes)
app.register_blueprint(bg_routes)
app.register_blueprint(jinja_filters.blueprint)


@app.before_request
def before_request():
    # database connection
    base_model.db.connect()


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


app.jinja_env.globals['csrf_token'] = generate_csrf_token

if not app.secret_key:
    app.secret_key = os.urandom(24)

csrf = CSRFProtect(app)

# allow running from the command line
if __name__ == '__main__':
    # app.run(use_reloader=False, debug=True)  # pythonista environment
    app.run()
