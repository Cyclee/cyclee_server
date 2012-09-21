import datetime
import json
from pyramid.config import Configurator
from pyramid.renderers import JSON
from sqlalchemy import engine_from_config
from geoalchemy.postgis import PGPersistentSpatialElement

from cyclee_server.models import DBSession, Base
from cyclee_server.views import RESTTrace, RESTRide


# FIX ME, find a better place for the adapter's for the JSON renderer
json_renderer = JSON()


def datetime_adapter(obj, request):
    return obj.isoformat()

json_renderer.add_adapter(datetime.datetime, datetime_adapter)


def pgelement_adapter(obj, request):
    # In order to pass a geometry object to the pyramid json renderer
    # we have to pull the geometry and generate a python dict
    # Postgis's geojson function returns a string, so we have to pass
    # that to json loads in order for the final output to be correct.

    # FIXME, this method currently makes a query against the database
    # for each geometry
    s = DBSession()
    return json.loads(s.scalar(obj.geojson))

json_renderer.add_adapter(PGPersistentSpatialElement, pgelement_adapter)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_renderer('json', json_renderer)

    config.add_route('home', '/')

    config.add_route('traces', '/traces')

    config.add_route('rest-trace', '/traces/{id}')

    config.add_view(RESTTrace,
                    attr='get',
                    renderer='json',
                    request_method='GET')
    config.add_view(RESTTrace,
                    attr='post',
                    renderer='json',
                    request_method='POST')

    config.add_view(RESTTrace,
                    attr='delete',
                    renderer='json',
                    request_method='DELETE')

    config.add_route('rides', '/rides')
    config.add_route('rest-rides', '/rides/{id}')

    config.add_view(RESTRide,
                    attr='get',
                    renderer='json',
                    request_method='GET')
    config.add_view(RESTRide,
                    attr='post',
                    renderer='json',
                    request_method='POST')

    config.add_view(RESTRide,
                    attr='delete',
                    renderer='json',
                    request_method='DELETE')

    config.scan()
    return config.make_wsgi_app()
