from urllib import parse
from markupsafe import Markup


def varencode(s):
    """
    URL encode string after first replacing spaces with underscores.
    :param s: String to url encode.
    :type s: basestring
    :return: URL-encoded string.
    """
    if type(s) == 'Markup':
        s = s.unescape()
    s = s.replace(' ', '_')
    s = s.encode('utf8')
    s = parse.quote_plus(s)
    return Markup(s)


def varunencode(s):
    """
    Unencode string url-encoded with varencode() to return it to its original readable state.
    :param s: String to unencode.
    :type s: basestring
    :return: Unencoded string.
    """
    s = s.replace('_', ' ')
    return parse.unquote(s)
