from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from cyclee_server.models import DBSession
from cyclee_server.views import RESTTrace


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')

    config.add_route('rest-traces', '/traces')

    config.add_route('rest-trace', '/traces/{id}')

    config.add_view(RESTTrace, attr='get', request_method='GET')
    config.add_view(RESTTrace, attr='post', request_method='POST')
    config.add_view(RESTTrace, attr='delete', request_method='DELETE')

    config.scan()
    return config.make_wsgi_app()
