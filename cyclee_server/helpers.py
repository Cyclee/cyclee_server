from pyramid.httpexceptions import HTTPNotFound
from cyclee_server.models import DBSession
import colander


class REST(object):

    resourceType = None
    schemaCls = None

    def get_resource(self):
        resource = self.session.query(
            self.resourceType).get(self.request.matchdict['id'])
        if resource is None:
            raise HTTPNotFound()
        return resource

    def __init__(self, request):
        self.request = request
        self.session = DBSession()

    def get(self):
        return self.get_resource()

    def post(self):
        resource = self.get_resource()
        s = self.schemaCls()
        vals = s.deserialize(self.request.json_body)
        for k, v in vals.items():
            setattr(resource, k, v)
        return resource

    def delete(self):
        self.session.delete(self.get_resource())
        return {'okay': True}


def process_form(request, form, post_validate_fn):
    if request.method == 'POST' and form.validate():
        return post_validate_fn(form)
    else:
        return {'form': form}


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
