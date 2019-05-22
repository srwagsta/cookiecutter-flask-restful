"""Extensions registry

All extensions here are used as singletons and
initialized in application factory
"""
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate{% if cookiecutter.use_celery == "yes" %}
from celery import Celery{% endif %}


db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
{%if cookiecutter.use_celery == "yes" %}
celery = Celery(){% endif %}
