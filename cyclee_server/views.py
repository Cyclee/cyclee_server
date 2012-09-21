from pyramid.response import Response
from pyramid.view import view_config
from pyramid.view import view_defaults
import colander

from cyclee_server.models import (
    DBSession, Trace, Ride
)

from cyclee_server.schemes import TraceSchema


@view_config(route_name='home', renderer='index.mako')
def index(request):
    return {}


@view_config(route_name='traces',
             renderer='json',
             request_method='GET')
def show_traces(request):
    session = DBSession()
    return [trace for trace in session.query(Trace).all()]


@view_config(route_name='rides',
             renderer='json',
             request_method='GET')
def show_rides(request):
    session = DBSession()
    return [ride for ride in session.query(Ride).all()]


def add_resource(request, model, schema_cls):
    session = DBSession()
    try:
        schema = schema_cls()
        vals = schema.deserialize(request.json_body)
        ints = model(**vals)
        session.add(ints)
        session.flush()
        return ints
    except colander.Invalid, e:
        request.response.status = 'Bad request 400'
        return e.asdict()


@view_config(route_name='traces',
             renderer='json',
             request_method='POST')
def add_trace(request):
    return add_resource(request, Trace, TraceSchema)


class REST(object):

    def get_resource(self):
        return self.session(
            self.resource).get(self.request.matchdict['id'])

    def __init__(self, request):
        self.request = request
        self.session = DBSession()


@view_defaults(route_name='rest-trace')
class RESTTrace(object):
    """A class that provides a restful interface to the trace object
       See Trace object for more details
    """

    def __init__(self, request):
        self.request = request

    def get(self):
        return Response()

    def post(self):
        return Response()

    def delete(self):
        return Response()


@view_defaults(route_name='rest-rides')
class RESTRide(object):

    def __init__(self, request):
        self.request = request

    def get(self):
        return Response()

    def post(self):
        return Response()

    def delete(self):
        return Response()
