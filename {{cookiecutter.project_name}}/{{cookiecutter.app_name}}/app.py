from flask import Flask

from {{cookiecutter.app_name}} import api
from {{cookiecutter.app_name}}.extensions import db, migrate{% if cookiecutter.use_celery == "yes"%}, celery{% endif%}


def create_app(testing=False, cli=False):
    """Application factory, used to create application
    """
    app = Flask('{{cookiecutter.app_name}}')
    app.config.from_object('{{cookiecutter.app_name}}.config')

    if testing is True:
        app.config['TESTING'] = True

    configure_extensions(app, cli)
    register_blueprints(app){% if cookiecutter.use_celery == "yes" %}
    init_celery(app){% endif %}

    return app


def configure_extensions(app, cli):
    """configure flask extensions
    """
    db.init_app(app)

    if cli is True:
        migrate.init_app(app, db)


def register_blueprints(app):
    """register all blueprints for application
    """
    app.register_blueprint(api.views.blueprint){% if cookiecutter.use_celery == "yes" %}


def init_celery(app=None):
    app = app or create_app()
    celery.conf.broker_url = app.config['CELERY_BROKER_URL']
    celery.conf.result_backend = app.config['CELERY_RESULT_BACKEND']
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        """Make celery tasks work with Flask app context"""
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery{% endif %}
