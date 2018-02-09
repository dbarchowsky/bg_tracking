import re
from flask import request, url_for, redirect
from bg_tracking.utils import varencode
from bg_tracking.controllers.utils import is_safe_url


def redirect_back(show, endpoint, **kwargs):
    target = request.form['next']
    if target:
        # update the show title and season in case they have changed after an edit
        target = re.sub(r'/show/.*/season/.*$',
                        r'/show/{}/season/{}'.format(varencode(show.title), show.season),
                        target)
    if not target or not is_safe_url(target):
        target = url_for(endpoint, **kwargs)
    return redirect(target)
