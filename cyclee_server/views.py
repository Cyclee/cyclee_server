from pyramid.view import view_config
from pyramid.view import view_defaults
from sqlalchemy.orm.exc import NoResultFound
# from pyramid.httpexceptions import HTTPNotFound

from wtforms import (
    Form,
    TextField,
    PasswordField,
    validators
)

from pyramid.httpexceptions import (
    HTTPFound,
)

from pyramid.security import (
    remember,
    forget,
)

from cyclee_server.models import (
    DBSession,
    User,
    Device,
    Trace,
    Ride
)

from cyclee_server.schemes import (
    TraceSchema,
    RideSchema,
    DeviceSchema
)
from cyclee_server.helpers import (
    REST,
    add_resource,
    process_form
)


class LoginForm(Form):
    name = TextField('Username', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])


@view_config(route_name='index', renderer='index.mako')
def index(request):
    return {}


@view_config(route_name='login', renderer='login.mako')
def login(request):
    form = LoginForm(request.POST)

    def post_validate(form):
        session = DBSession()
        try:
            user = session.query(User).filter_by(
                name=form.name.data,
                password=User.encode_password(form.password.data)).one()
            headers = remember(request, user.id)
            return HTTPFound(
                headers=headers,
                location=request.route_url('index'))
        except NoResultFound, e:
            return {'form': form, 'errors': [e]}

    return process_form(
        request,
        form,
        post_validate
    )


@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(
        headers=headers,
        location=request.route_url('index')
    )


##############################
# API Views
##############################


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


@view_config(route_name='devices',
             renderer='json',
             request_method='GET')
def show_devices(request):
    session = DBSession()
    return list(session.query(Device).all())


@view_config(route_name='traces',
             renderer='json',
             request_method='POST')
def add_trace(request):
    return add_resource(request, Trace, TraceSchema)


@view_config(route_name='rides',
             renderer='json',
             request_method='POST')
def add_ride(request):
    return add_resource(request, Ride, RideSchema)


@view_config(route_name='devices',
             renderer='json',
             request_method='POST')
def add_device(request):
    return add_resource(request, Device, DeviceSchema)


@view_defaults(route_name='rest-trace')
class RESTTrace(REST):
    """A class that provides a restful interface to the trace object
       See Trace object for more details
    """
    resourceType = Trace
    schemaCls = TraceSchema


@view_defaults(route_name='rest-rides')
class RESTRide(REST):

    resourceType = Ride
    schemaCls = RideSchema


@view_defaults(route_name='rest-devices')
class RESTDevice(REST):

    resourceType = Device
    schemaCls = DeviceSchema
