from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey
)

from geoalchemy import (
    GeometryColumn,
    Point,
    GeometryDDL
)

from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    #relationship,
    sessionmaker
)
from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(
    sessionmaker(
        autoflush=True,
        extension=ZopeTransactionExtension()
    )
)

Base = declarative_base()


class ResourceMixin(object):
    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime, default=func.now())

    def __json__(self, request):
        d = {}
        for c in self.__table__.columns:
            d[c.name] = getattr(self, c.name)
        return d


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    date_joined = Column(DateTime, default=func.now())
    age = Column(Integer)
    gender = Column(String)


class Device(Base, ResourceMixin):
    __tablename__ = 'devices'

    type = Column(String)
    owner_id = Column(Integer, ForeignKey('users.id'))


class Ride(Base, ResourceMixin):
    __tablename__ = 'rides'

    time_started = Column(DateTime)
    time_ended = Column(DateTime)
    owner_id = Column(Integer, ForeignKey('users.id'))


class Trace(Base, ResourceMixin):
    __tablename__ = 'traces'

    geometry = GeometryColumn(Point(2))
    altitude = Column(Float)
    device_timestamp = Column(DateTime)  # The time from the device
    ride_id = Column(Integer, ForeignKey('users.id'))


GeometryDDL(Trace.__table__)
