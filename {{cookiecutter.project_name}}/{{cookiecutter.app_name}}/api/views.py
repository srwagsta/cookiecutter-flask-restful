from flask import Blueprint
from flask_restful import Api

from {{cookiecutter.app_name}}.api.resources import ExampleResource, ExampleList


blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint)


api.add_resource(ExampleResource, '/example/<int:example_id>')
api.add_resource(ExampleList, '/examples')
