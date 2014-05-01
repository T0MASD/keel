import unittest

from pyramid import testing


class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_my_view(self):
        from ..views.projects import get_projects
        request = testing.DummyRequest()
        projects = get_projects(request)
        self.assertEqual(projects, {'projects': ['Project 1', 'Project 2', 'Project 3']})
