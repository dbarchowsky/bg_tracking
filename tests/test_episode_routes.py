import unittest
from flask import Flask, request
import bg_tracking


class EpisodeRoutesTestCase(unittest.TestCase):

    """
    Tests Show-related page content.
    """
    def setUp(self):
        bg_tracking.app.testing = True
        self.app = Flask(__name__)
        self.atc = bg_tracking.app.test_client()

    def test_edit_new_with_show_id(self):
        show_id = 2
        route = '/episode/edit/?show_id={}'.format(show_id)
        with self.app.test_request_context(route):
            assert int(request.args.get('show_id')) == show_id

    def test_edit_new_with_missing_show_id(self):
        route = '/episode/edit'
        with self.app.test_request_context(route):
            self.assertIsNone(request.args.get('show_id'))

    def test_edit_existing(self):
        episode_id = 4
        route = '/episode/{}/edit'.format(episode_id)
        response = self.atc.get(route, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_default_details_view(self):
        episode_id = 1
        route = '/episode/{}'.format(episode_id)
        response = self.atc.get(route, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # assert b'<title>Error</title>' in response.data


if __name__ == '__main__':
    unittest.main()
