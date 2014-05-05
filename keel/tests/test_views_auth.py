import unittest
from pyramid import testing

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
        userid = 'hank'
        self.config.testing_securitypolicy(userid=userid)
        request = testing.DummyRequest()
        response = logout(request)
        self.assertEqual(response, {'status': 'Logged out %s' % userid})


    def test_auth_view(self):
        from ..views.auth import auth
        request = testing.DummyRequest()
        response = auth(request)
        self.assertEqual(response, 'See console')


class IntegrationTests(unittest.TestCase):
    def setUp(self):
        from webtest import TestApp
        from pyramid.paster import get_app
        app = get_app('development.ini')
        self.app = TestApp(app)


    def tearDown(self):
        testing.tearDown()


    def test_login_view(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_int, 200)


    def test_logout_view(self):
        # run login to start session
        self.app.get('/login')
        response = self.app.get('/logout')
        self.assertEqual(response.status_int, 200)


    def test_logout_not_loggedin(self):
        # expect 403 when trying to log out again
        from pyramid.httpexceptions import HTTPForbidden
        response = self.app.get('/logout', expect_errors=True)
        self.assertEqual(response.status_int, 403)
