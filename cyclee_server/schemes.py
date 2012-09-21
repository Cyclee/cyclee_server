from colander import (
    MappingSchema,
    SchemaNode,
    Integer,
    String,
    DateTime
)


class DeviceSchema(MappingSchema):
    type = String()
    owner_id = Integer()


class UserSchema(MappingSchema):
    name = SchemaNode(String())
    email = SchemaNode(String())
    password = SchemaNode(String())
    age = SchemaNode(String())
    gender = SchemaNode(String())


class GeometrySchema(MappingSchema):
    x = SchemaNode(Integer())
    y = SchemaNode(Integer())


class TraceSchema(MappingSchema):
    altitude = SchemaNode(Integer())
    ride_id = SchemaNode(Integer())
    device_timestamp = SchemaNode(DateTime())
    geometry = SchemaNode(String())


class RideSchema(MappingSchema):
    time_started = SchemaNode(DateTime())
    time_ended = SchemaNode(DateTime())
    owner_id = SchemaNode(Integer())
