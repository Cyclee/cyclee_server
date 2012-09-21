import yaml
import argparse
import transaction
from zope.dottedname.resolve import resolve
from pyramid.paster import get_appsettings
from sqlalchemy import engine_from_config

from cyclee_server.models import DBSession, Base


class Command(object):

    def __init__(self, **kwargs):
        pass


def clear_database(engine):
    DBSession.configure(bind=engine)
    Base.metadata.drop_all(engine)


def load_database(engine):
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)


def load_fixtures(fixture_path):
    fixtures = yaml.load(open(fixture_path, 'r').read())
    session = DBSession()

    for fixture in fixtures:
        model = resolve(fixture.get('class'))
        try:
            inst = model(**fixture['fields'])
            with transaction.manager:
                session.add(inst)
        except Exception, e:
            raise e


def clear_command():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--settings',
        help='The settings ini file')
    args = parser.parse_args()
    settings = get_appsettings(args.settings)
    engine = engine_from_config(settings, 'sqlalchemy.')
    clear_database(engine)


def fixture_command():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--fixtures',
        dest='path',
        help='The fixtures yaml file')
    parser.add_argument(
        '--settings',
        dest='settings',
        help='The settings ini file')
    args = parser.parse_args()
    settings = get_appsettings(args.settings)
    engine = engine_from_config(settings, 'sqlalchemy.')
    load_database(engine)
    load_fixtures(args.path)
