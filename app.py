from flask import Flask
from flask import render_template
from bg_tracking import *
app = Flask(__name__)


@app.before_request
def before_request():
    base_model.db.connect()


@app.after_request
def after_request(response):
    base_model.db.close()
    return response


@app.route('/')
def list_bgs():
    return 'Hello.'


@app.route('/show/<show>')
def list_episodes(show):
    """
    List the episodes available in the requested show.
    :param show: Show name
    :return: Response
    """
    return 'Show is "{}"'.format(show)


@app.route('/episode/<episode_id>')
def show_episode(episode_id):
    """
    List backgrounds in the requested episode.
    :param episode_id:
    :return:
    """
    e = Episode.get(Episode.id == episode_id)
    bgs = Background.select().where(Background.episode == episode_id).order_by(Background.scene)
    return render_template('episode.html', episode=e, bgs=bgs)


# allow running from the command line
if __name__ == '__main__':
    app.run()