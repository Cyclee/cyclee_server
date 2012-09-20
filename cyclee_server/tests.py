import unittest


from pyramid import testing

from .models import DBSession, Base


class TestBase(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine
        engine = create_engine('postgresql://postgres:@localhost/cyclee_test')
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()


mock_trace = {
    'geometry': {'x': 42, 'y': -73},
    'altitude': 10,
    'ride_1': 1,
    'device_timestamp': 'Date'
}


class TestAddTrace(TestBase):

    def setUp(self):
        super(TestAddTrace, self).setUp()

    def tearDown(self):
        super(TestAddTrace, self).tearDown()

    def test_adding_trace(self):
        from .views import add_trace
        request = testing.DummyRequest()
        request.params = mock_trace
        resp = add_trace(request)
        print resp


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
        print resp
