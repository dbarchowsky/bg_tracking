import unittest
import bg_tracking


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
        rv = self.app.get('/show/{}'.format(show_title), follow_redirects=True)
        assert b'<title>Error - BG Tracker</title>' in rv.data
        assert b'<h1>Error</h1>' in rv.data
        s = '<p class="alert alert-error">The show &#34;{}&#34; was not found.</p>'.format(unencoded)
        assert bytes(s, encoding='utf-8') in rv.data


if __name__ == '__main__':
    unittest.main()
