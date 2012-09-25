import hashlib
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
    relationship,
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


def groupfinder(userid, request):
    pass


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

    devices = relationship('Device', backref='user')
    rides = relationship('Ride', backref='user')

    @staticmethod
    def encode_password(passwd_str):
        return hashlib.md5(passwd_str).hexdigest()


class Device(Base, ResourceMixin):
    __tablename__ = 'devices'

    type = Column(String)
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship(
        'User',
        cascade='all, delete',
        primaryjoin='User.id==Device.owner_id'
    )


class Ride(Base, ResourceMixin):
    __tablename__ = 'rides'

    time_started = Column(DateTime)
    time_ended = Column(DateTime)
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship(
        'User',
        cascade='all, delete',
        primaryjoin='User.id==Ride.owner_id'
    )


class Trace(Base, ResourceMixin):
    __tablename__ = 'traces'

    geometry = GeometryColumn(Point(2))
    altitude = Column(Float)
    device_timestamp = Column(DateTime)  # The time from the device
    ride_id = Column(Integer, ForeignKey('rides.id'))
    ride = relationship(
        'Ride',
        cascade='all, delete',
        primaryjoin='Ride.id==Trace.ride_id'
    )


GeometryDDL(Trace.__table__)
