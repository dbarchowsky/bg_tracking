import string
import random
from urllib.parse import urlparse, urljoin
from flask import session, abort, request, redirect, url_for


def get_or_404(query, *expr):
    try:
        return query.where(*expr).get()
    except query.model_class.DoesNotExist:
        abort(404)


def generate_random_string(size=6, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = generate_random_string(12)
    return session['_csrf_token']


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def get_redirect_target():
    for target in request.values.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target


def redirect_back(endpoint, **kwargs):
    target = request.form['next']
    if not target or not is_safe_url(target):
        target = url_for(endpoint, **kwargs)
    return redirect(target)
