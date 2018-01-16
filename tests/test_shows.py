import unittest
import bg_tracking
from bg_tracking.models import *


class ShowTestCase(unittest.TestCase):
    """
    Tests Show-related page content.
    """
    def setUp(self):
        bg_tracking.app.testing = True
        self.app = bg_tracking.app.test_client()

    def test_show_list(self):
        rv = self.app.get('/shows', follow_redirects=True)
        assert b'<title>Shows - BG Tracker</title>' in rv.data
        assert b'<h1>Shows</h1>' in rv.data

    def test_unknown_show_title(self):
        show_title = 'bogus_title'
        unencoded = bg_tracking.varunencode(show_title)
        rv = self.app.get('/show/{}/season/1'.format(show_title), follow_redirects=True)
        assert b'<title>Error - BG Tracker</title>' in rv.data
        assert b'<h1>Error</h1>' in rv.data
        s = '<p class="alert alert-error">The show &#34;{}&#34; was not found.</p>'.format(unencoded)
        assert bytes(s, encoding='utf-8') in rv.data

    def test_show_details_by_title(self):

        # get most recent show
        base_model.db.connect()
        s = Show.select().order_by(Show.id.desc()).get()
        base_model.db.close()

        route = '/show/{}/season/{}'.format(bg_tracking.varencode_filter(s.name), s.season)
        response = self.app.get(route, follow_redirects=True)

        title_test = '<title>{} season {} - BG Tracker</title>'.format(s.name, s.season)
        header_test = '<h1>{} season {}</h1>'.format(s.name, s.season)
        assert bytes(title_test, encoding='utf-8') in response.data
        assert bytes(header_test, encoding='utf-8') in response.data

    def test_show_details_by_title_route(self):

        # get most recent show
        base_model.db.connect()
        s = Show.select().order_by(Show.id.desc()).get()
        base_model.db.close()

        route = '/show/{}/season/{}'.format(bg_tracking.varencode_filter(s.name), s.season)
        response = self.app.get(route, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_show_details_by_title_route_mission_season(self):
        response = self.app.get('/show/Close_Enough', follow_redirects=True)
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
