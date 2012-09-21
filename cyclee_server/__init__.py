import datetime
from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from cyclee_server.models import DBSession, Base
from cyclee_server.views import RESTTrace

from pyramid.renderers import JSON

# FIX ME, find a better place for the adapter's for the JSON renderer
json_renderer = JSON()


def datetime_adapter(obj, request):
    return obj.isoformat()

json_renderer.add_adapter(datetime.datetime, datetime_adapter)


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

    config.add_view(RESTTrace, attr='get', request_method='GET')
    config.add_view(RESTTrace, attr='post', request_method='POST')
    config.add_view(RESTTrace, attr='delete', request_method='DELETE')

    config.add_route('rides', '/rides')

    config.scan()
    return config.make_wsgi_app()
