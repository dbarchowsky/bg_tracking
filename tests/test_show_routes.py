import unittest
from flask import Flask, request
import bg_tracking
from bg_tracking.models import *


class ShowRoutesTestCase(unittest.TestCase):
    """
    Tests Show-related page content.
    """
    def setUp(self):
        bg_tracking.app.testing = True
        self.app = Flask(__name__)
        self.atc = bg_tracking.app.test_client()

    def test_show_list(self):
        rv = self.atc.get('/shows', follow_redirects=True)
        assert b'<title>Shows - BG Tracker</title>' in rv.data
        assert b'<h1>Shows</h1>' in rv.data

    def test_unknown_show_title(self):
        show_title = 'bogus_title'
        unencoded = bg_tracking.varunencode(show_title)
        rv = self.atc.get('/show/{}/season/1'.format(show_title), follow_redirects=True)
        assert b'<title>Error - BG Tracker</title>' in rv.data
        assert b'<h1>Error</h1>' in rv.data
        s = '<p class="alert alert-error">The show &#34;{}&#34; was not found.</p>'.format(unencoded)
        assert bytes(s, encoding='utf-8') in rv.data

    def test_show_details_by_title(self):

        # get most recent show
        base_model.db.connect()
        s = Show.select().order_by(Show.id.desc()).get()
        base_model.db.close()

        route = '/show/{}/season/{}'.format(bg_tracking.varencode(s=s.title), s.season)
        response = self.atc.get(route, follow_redirects=True)

        title_test = '<title>{} season {} - BG Tracker</title>'.format(s.title, s.season)
        header_test = '<h1>{} season {}</h1>'.format(s.title, s.season)
        assert bytes(title_test, encoding='utf-8') in response.data
        assert bytes(header_test, encoding='utf-8') in response.data

    def test_show_details_by_title_route(self):

        # get most recent show
        base_model.db.connect()
        s = Show.select().order_by(Show.id.desc()).get()
        base_model.db.close()

        route = '/show/{}/season/{}'.format(bg_tracking.varencode(s=s.title), s.season)
        response = self.atc.get(route, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_show_details_by_title_route_mission_season(self):
        response = self.atc.get('/show/Close_Enough', follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    def test_new_show_form(self):
        route = '/show/edit'
        response = self.atc.get(route)
        self.assertEqual(response.status_code, 200)

    def test_existing_show_form(self):
        show_id = 2
        route = '/show/{}/edit'.format(show_id)
        response = self.atc.get(route)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
