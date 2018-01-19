from flask import Blueprint
import jinja2
from urllib import parse
from markupsafe import Markup

blueprint = Blueprint('jinja_filters', __name__)


@jinja2.contextfilter
@blueprint.app_template_filter()
def varencode(context, s):
    """
    URL encodes string, after replacing spaces with underscores.
    Formats show titles in expected format for including in routes.
    :param s: String to encode
    :type s: basestring
    :return: URL encoded string.
    """
    if type(s) == 'Markup':
        s = s.unescape()
    s = s.replace(' ', '_')
    s = s.encode('utf8')
    s = parse.quote_plus(s)
    return Markup(s)


@jinja2.contextfilter
@blueprint.app_context_processor
def bg_size_css_class():
    def _bg_size_css_class(w, h):
        """
        Returns css class name corresponding to the size of the BG.
        :param w: BG width in pixels
        :type w: int
        :param h: BG height in pixels
        :type h: int
        :return: CSS class name to insert into template.
        """
        base_area = 4500 * 2500
        bg_area = w * h
        if bg_area > (base_area * 1.9):
            return 'bg-sized-xxl'
        elif bg_area > (base_area * 1.5):
                return 'bg-sized-xl'
        elif bg_area > (base_area):
            return 'bg-sized-lg'
        else:
            return 'bg-sized-base'
    return dict(bg_size_css_class=_bg_size_css_class)

