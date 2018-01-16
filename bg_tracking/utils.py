from urllib import parse


def varunencode(s):
    s = s.replace('_', ' ')
    return parse.unquote(s)
