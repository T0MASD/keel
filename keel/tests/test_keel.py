import unittest
from pyramid import testing


class KeelTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()


    def tearDown(self):
        testing.tearDown()


    def test_groupfinder(self):
        from keel import groupfinder
        request = testing.DummyRequest()
        username = 'adminuser'
        groups = groupfinder(username, request)
        self.assertEqual(groups, ['g:admin'])
