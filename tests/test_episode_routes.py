import unittest
from datetime import datetime
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
        route = '/episode/add/?show_id={}'.format(show_id)
        with self.app.test_request_context(route):
            assert int(request.args.get('show_id')) == show_id

    def test_edit_new_with_missing_show_id(self):
        route = '/episode/add'
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

    def tet_submit_new_record(self):
        data = {'title': 'unit test {:%Y%d%m}'.format(datetime.now()),
                'number': 1,
                'show': 3,
                'id': None
                }
        response = self.atc.post('/episode/add/', data=data)
        self.assertEqual(response.status_code, 200)

    def _out_test_submit_new_record(self):
        data = {'title': 'unit test {:%Y%d%m}'.format(datetime.now()),
                'number': 1,
                'show': 3,
                'id': None
                }
        with self.app.test_request_context('/episode/add/',
                                           method='POST',
                                           data=data
                                           ):
            rv = self.app.preprocess_request()
            if rv is not None:
                response = self.app.make_response(rv)
            else:
                rv = self.app.dispatch_request()
                response = self.app.make_response(rv)
                response = self.app.process_response(response)

            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
