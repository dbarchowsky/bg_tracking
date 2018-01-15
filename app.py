from flask import Flask
from flask import render_template
import urllib
from markupsafe import Markup
from bg_tracking import *
app = Flask(__name__)


def varunencode(s):
    s = s.replace('_', ' ')
    return urllib.parse.unquote(s)


@app.before_request
def before_request():
    base_model.db.connect()


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

@app.route('/episodes/')
def episode_list():
    episodes = (Episode
        .select()
        .join(Show)
        .order_by(Show.name, Episode.number)
        )
    return render_template('episode_list.html', title='Episodes', episodes=episodes)

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
        msg = 'The requested show was not found. (id:{})'.format(show_id)
        return render_template('error.html', error_msg=msg)
    else:
        title = "{} season {}".format(show.name, show.season)
        try:
            episodes = Episode.select().where(Episode.show == show.id)
        except:
            title = 'Error retrieving episodes in {}'.format(show.name)
    return render_template('show_detail.html', title=title, show=show, episodes=episodes)


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

# allow running from the command line
if __name__ == '__main__':
    app.run()
