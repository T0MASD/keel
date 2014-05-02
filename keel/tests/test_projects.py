import unittest
from pyramid import testing


class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()


    def tearDown(self):
        testing.tearDown()


    def test_get_projects_view(self):
        from ..views.projects import get_projects
        request = testing.DummyRequest()
        projects = get_projects(request)
        self.assertEqual(projects, {'projects': ['Project 1', 'Project 2', 'Project 3']})


class IntegrationTests(unittest.TestCase):
    def setUp(self):
        from webtest import TestApp
        from pyramid.paster import get_app
        app = get_app('development.ini')
        self.app = TestApp(app)


    def tearDown(self):
        testing.tearDown()


    def test_projects_view(self):
        # run login to start session
        login = self.app.get('/login')
        csrf_token = login.json_body['csrf_token']
        response = self.app.get('/projects?csrf_token=%s' % csrf_token)
        self.assertEqual(response.status_int, 200)
