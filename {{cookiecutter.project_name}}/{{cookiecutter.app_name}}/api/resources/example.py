from flask import request
from flask_restful import Resource
from {{cookiecutter.app_name}}.commons.decorators import token_required
from {{cookiecutter.app_name}}.models import Example
from {{cookiecutter.app_name}}.extensions import ma, db
from {{cookiecutter.app_name}}.commons.pagination import paginate


class ExampleSchema(ma.ModelSchema):

    class Meta:
        model = Example
        sqla_session = db.session


class ExampleResource(Resource):
    """Single object resource
    """
    method_decorators = [token_required]

    def get(self, example_id):
        schema = ExampleSchema()
        entry = Example.query.get_or_404(example_id)
        return {"entry": schema.dump(entry).data}

    def put(self, example_id):
        schema = ExampleSchema(partial=True)
        entry = Example.query.get_or_404(example_id)
        entry, errors = schema.load(request.json, instance=entry)
        if errors:
            return errors, 422

        return {"msg": "example updated", "entry": schema.dump(entry).data}

    def delete(self, example_id):
        entry = Example.query.get_or_404(example_id)
        db.session.delete(entry)
        db.session.commit()

        return {"msg": "example entry deleted"}


class ExampleList(Resource):
    """Creation and get_all
    """
    method_decorators = [token_required]

    def get(self):
        schema = ExampleSchema(many=True)
        query = Example.query
        return paginate(query, schema)

    def post(self):
        schema = ExampleSchema()
        entry, errors = schema.load(request.json)
        if errors:
            return errors, 422

        db.session.add(entry)
        db.session.commit()

        return {"msg": "example entry created", "example": schema.dump(entry).data}, 201
