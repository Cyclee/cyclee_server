from colander import (
    MappingSchema,
    SchemaNode,
    Integer,
    DateTime
)


class GeometrySchema(MappingSchema):
    x = SchemaNode(Integer())
    y = SchemaNode(Integer())


class TraceSchema(MappingSchema):
    altitude = SchemaNode(Integer())
    ride_id = SchemaNode(Integer())
    device_timestamp = SchemaNode(DateTime())
    geometry = GeometrySchema()


class TraceRide(MappingSchema):
    time_started = SchemaNode(DateTime())
    time_ended = SchemaNode(DateTime())
    owner_id = SchemaNode(Integer())
