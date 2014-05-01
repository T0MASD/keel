import unittest
from webtest import TestApp
from pyramid import testing
from pyramid.paster import get_app


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
        #self.config = testing.setUp()
        app = get_app('development.ini')
        self.app = TestApp(app)


    def tearDown(self):
        testing.tearDown()


    # def test_projects_view(self):
    #     response = self.app.get('/projects')
        # Needs to be logged in and have valid token
        #self.assertEqual(response.status_int, 200)
