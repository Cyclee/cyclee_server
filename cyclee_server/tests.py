import unittest


from pyramid import testing

from cyclee_server.scripts import (
    load_database,
    clear_database,
    load_fixtures
)

from .models import DBSession, Base


class TestBase(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine

        self.engine = create_engine(
            'postgresql://postgres:@localhost/cyclee_test'
        )

        DBSession.configure(bind=self.engine)
        Base.metadata.create_all(self.engine)
        load_database(self.engine)
        load_fixtures('fixtures.yml')

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

mock_ride = {
    'owner_id': 1,
    'time_started': '2007-01-25T12:00:00Z',
    'time_ended': '2007-01-25T12:00:00Z'
}

mock_trace = {
    'geometry': 'POINT(-88.5945861592357 42.9480095987261)',
    'altitude': 10,
    'ride_id': 1,
    'device_timestamp': '2007-01-25T12:00:00Z'
}


class TestAddGetTrace(TestBase):

    def setUp(self):
        super(TestAddGetTrace, self).setUp()

    def tearDown(self):
        super(TestAddGetTrace, self).tearDown()

    def test_adding_trace(self):
        from .views import add_trace
        from .models import Trace
        request = testing.DummyRequest()
        request.json_body = mock_trace
        resp = add_trace(request)
        self.assertTrue(isinstance(resp, Trace))

    def test_adding_bad_trace(self):
        from .views import add_trace
        request = testing.DummyRequest()
        request.json_body = {'key': 'not right key'}
        resp = add_trace(request)
        self.assertTrue(isinstance(resp, dict))
        self.assertTrue(len(resp.keys()), 4)


class TestRESTTrace(TestBase):

    def setUp(self):
        super(TestRESTTrace, self).setUp()

    def tearDown(self):
        super(TestRESTTrace, self).tearDown()

    def test_get(self):
        from .views import RESTTrace
        request = testing.DummyRequest()
        request.matchdict = {'id': u'1'}
        rest = RESTTrace(request)
        resp = rest.get()
        print resp

    def test_post(self):
        from .views import RESTTrace
        request = testing.DummyRequest()
        request.params = mock_trace
        rest = RESTTrace(request)
        resp = rest.post()
        # print resp
