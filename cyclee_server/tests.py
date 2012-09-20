import unittest
import transaction

from pyramid import testing

from .models import DBSession, Base


class TestRESTTrace(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine
        engine = create_engine('postgresql://postgres:@localhost/cyclee_test')
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_get(self):
        from .views import RESTTrace
        request = testing.DummyRequest()
        rest = RESTTrace(request)
        resp = rest.get()
        print resp

    def test_post(self):
        from .views import RESTTrace
        request = testing.DummyRequest()
        rest = RESTTrace(request)
        resp = rest.post()
        print resp
