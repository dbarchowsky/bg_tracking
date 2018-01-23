import unittest
from flask import Flask, request
import bg_tracking


class BgRoutesTestCase(unittest.TestCase):

    """
    Tests Background-related routes.
    """
    def setUp(self):
        bg_tracking.app.testing = True
        self.app = bg_tracking.app.test_client()

    def test_landing(self):
        response = self.app.get('/', follow_redirects=True)
        assert b'<h1>BGs</h1>' in response.data

    def test_bg_listings(self):
        response = self.app.get('/bgs')
        assert b'<h1>BGs</h1>' in response.data

    def test_bg_listings_sorted(self):
        response = self.app.get('/bgs/sorted/by/hours')
        assert b'<h1>BGs</h1>' in response.data

    def test_bg_listings_sorted_desc(self):
        response = self.app.get('/bgs/sorted/by/hours/desc')
        self.assertEqual(response.status_code, 200)

    def test_bg_listings_sorted_by_invalid_criteria(self):
        response = self.app.get('/bgs/sorted/by/bogus_criteria')
        s = '<p class="alert alert-error">Invalid sort criteria.</p>'
        assert bytes(s, encoding='utf-8') in response.data

    def test_edit_new_bg(self):
        response = self.app.get('/bg/edit', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
