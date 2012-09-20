from pyramid.response import Response
from pyramid.view import view_config
from pyramid.view import view_defaults
import colander

from cyclee_server.schemas import TraceSchema


@view_config(route_name='home', renderer='index.mako')
def index(request):
    return {}


@view_config(route_name='rest-traces', request_method='GET')
def show_traces(request):
    return {}


@view_config(route_name='rest-traces', request_method='POST')
def add_trace(request):
    schema = TraceSchema()
    try:
        schema.deserialize(request.params)
    except colander.Invalid, e:
        return {'errors': e.asdict()}


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
