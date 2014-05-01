import unittest
from webtest import TestApp
from pyramid import testing
from pyramid.paster import get_app

class UnitTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()


    def tearDown(self):
        testing.tearDown()


    def test_login_view(self):
        from ..views.auth import login
        request = testing.DummyRequest()
        response = login(request)
        self.assertEqual(response['username'], 'manageruser')
        self.assertEqual(len(response['csrf_token']), len('0123456789012345678901234567890123456789'))


    def test_logout_view(self):
        from ..views.auth import logout
        request = testing.DummyRequest()
        response = logout(request)
        self.assertEqual(response, {'status': 'Logged out None'})        


class IntegrationTests(unittest.TestCase):
    def setUp(self):
        #self.config = testing.setUp()
        app = get_app('development.ini')
        self.app = TestApp(app)


    def tearDown(self):
        testing.tearDown()


    def test_login_view(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_int, 200)


    # def test_logout_view(self):
    #     response = self.app.get('/logout')
        # Needs to be logged in
        #self.assertEqual(response.status_int, 200)
