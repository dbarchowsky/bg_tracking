from math import floor
from flask import Blueprint
import jinja2
import bg_tracking

blueprint = Blueprint('jinja_filters', __name__)


@jinja2.contextfilter
@blueprint.app_template_filter()
def varencode(context, s):
    """
    URL encodes string, after replacing spaces with underscores.
    Formats show titles in expected format for including in controllers.
    :param context: Template context parameter
    :param s: String to encode
    :type s: basestring
    :return: URL encoded string.
    """
    return bg_tracking.varencode(s)


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


@jinja2.contextfilter
@blueprint.app_context_processor
def css_pct():
    def _css_pct(total, n):
        """
        Returns value to insert as percentage value in CSS selector
        :param total: total number of items
        :param n: items in set
        :return: formatted percentage value
        """
        return floor((n/total) * 10) * 10
    return dict(css_pct=_css_pct)


@jinja2.contextfilter
@blueprint.app_context_processor
def format_percent():
    def _format_percent(total, n):
        """
        Formats percentage value
        :param total: total number of items
        :param n: items in set
        :return: formatted percentage value
        """
        return '{}%'.format(round((n/total) * 100))
    return dict(format_percent=_format_percent)
