import string
import random
from flask import session, abort


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
