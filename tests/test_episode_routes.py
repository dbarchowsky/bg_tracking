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

    def test_edit_new_with_show_id(self):
        show_id = 2
        route = '/episode/edit/?show_id={}'.format(show_id)
        with self.app.test_request_context(route):
            assert int(request.args.get('show_id')) == show_id

    def test_edit_new_with_missing_show_id(self):
        route = '/episode/edit'
        with self.app.test_request_context(route):
            self.assertIsNone(request.args.get('show_id'))


if __name__ == '__main__':
    unittest.main()
