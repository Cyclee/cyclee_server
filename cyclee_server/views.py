from pyramid.response import Response
from pyramid.view import view_config
from pyramid.view import view_defaults
from pyramid.httpexceptions import HTTPNotFound

import colander

from cyclee_server.models import (
    DBSession, Trace, Ride
)

from cyclee_server.schemes import TraceSchema


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


@view_config(route_name='home', renderer='index.mako')
def index(request):
    return {}


@view_config(route_name='traces',
             renderer='json',
             request_method='GET')
def show_traces(request):
    session = DBSession()
    return list(session.query(Trace).all())


@view_config(route_name='rides',
             renderer='json',
             request_method='GET')
def show_rides(request):
    session = DBSession()
    return list(session.query(Ride).all())


@view_config(route_name='traces',
             renderer='json',
             request_method='POST')
def add_trace(request):
    return add_resource(request, Trace, TraceSchema)


class REST(object):

    resource = None

    def get_resource(self):
        resource = self.session.query(
            self.resource).get(self.request.matchdict['id'])
        if resource is None:
            raise HTTPNotFound()
        return resource

    def __init__(self, request):
        self.request = request
        self.session = DBSession()

    def get(self):
        return self.get_resource()

    def post(self):
        return {}

    def delete(self):
        self.session.delete(self.get_resource())
        return {'okay': True}


@view_defaults(route_name='rest-trace')
class RESTTrace(REST):
    """A class that provides a restful interface to the trace object
       See Trace object for more details
    """
    resource = Trace


@view_defaults(route_name='rest-rides')
class RESTRide(object):

    resource = Ride
