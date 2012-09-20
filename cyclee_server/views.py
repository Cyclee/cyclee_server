from pyramid.response import Response
from pyramid.view import view_config
from pyramid.view import view_defaults


@view_config(route_name='home', renderer='index.mako')
def index(request):
    return {}


@view_defaults(route_name='rest-traces')
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
