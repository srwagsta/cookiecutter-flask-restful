# cookiecutter-flask-restful

Cookiecutter template for flask restful, including blueprints, application factory, and more

## Introduction

This cookie cutter is a very simple boilerplate for starting a REST api using Flask, flask-restful, marshmallow, SQLAlchemy.
It comes with basic project structure and configuration, including blueprints, application factory and basics unit tests.

Features

* Simple flask application using application factory, blueprints
* [Flask command line interface](http://flask.pocoo.org/docs/1.0/cli/) integration
* Simple cli implementation with basics commands (init, run, etc.)
* [Flask Migrate](https://flask-migrate.readthedocs.io/en/latest/) included in entry point
* Authentication using outside authority. This assumes you have an auth api handeling JWT.
* Simple pagination utils
* Unit tests using pytest and factoryboy
* Configuration using environment variables

Used packages :

* [Flask](http://flask.pocoo.org/)
* [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/)
* [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/)
* [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/)
* [Flask-Marshmallow](https://flask-marshmallow.readthedocs.io/en/latest/)
* [marshmallow-sqlalchemy](https://marshmallow-sqlalchemy.readthedocs.io/en/latest/)
* [tox](https://tox.readthedocs.io/en/latest/)
* [pytest](https://docs.pytest.org/en/latest/)
* [factoryboy](http://factoryboy.readthedocs.io/en/latest/)
* [dotenv](https://github.com/theskumar/python-dotenv)


## Usage

### Installation

For the example, let's say you named your app `myapi` and your project `myproject`

Once project started with cookiecutter, you can install it using pip :

```
cd myproject
pip install -r requirements.txt
pip install -e .
```

You have now access to cli commands and you can init your project

```
myapi init
```

To list all commands

```
myapi --help
```

### Configuration

Configuration is handled by environment variables, for development purpose you just
need to update / add entries in `.flaskenv` file.

It's filled by default with following content:

```
FLASK_ENV=development
FLASK_APP="myapp.app:create_app"
SECRET_KEY=changeme
DATABASE_URI="sqlite:////tmp/myapp.db"
CELERY_BROKER_URL=amqp://guest:guest@localhost/  # only present when celery is enabled
CELERY_RESULT_BACKEND_URL=amqp://guest:guest@localhost/  # only present when celery is enabled
```

Avaible configuration keys:

* `FLASK_ENV`: flask configuration key, enables `DEBUG` if set to `development`
* `SECREY_KEY`: your application secret key
* `DATABASE_URI`: SQLAlchemy connection string
* `CELERY_BROKER_URL`: URL to use for celery broker, only when you enabled celery
* `CELERY_RESULT_BACKEND_URL`: URL to use for celery result backend (e.g: `redis://localhost`)


### Running tests

Simplest way to run tests is to use tox, it will create a virtualenv for tests, install all dependencies and run pytest

```
tox
```

But you can also run pytest manually, you just need to install tests dependencies before

```
pip install pytest pytest-runner pytest-flask pytest-factoryboy factory_boy
pytest
```

**WARNING**: you will need to set env variables

### Running with gunicorn

This project provide a simple wsgi entry point to run gunicorn or uwsgi for example.

For gunicorn you only need to run the following commands

```
pip install gunicorn
gunicorn myapi.wsgi:app
```

And that's it ! Gunicorn is running on port 8000


### Using Flask CLI

This cookiecutter is fully compatible with default flask CLI and use a `.flaskenv` file to set correct 
env variables to bind the application factory.
Note that we also set `FLASK_ENV` to `development` to enable debugger.


### Using Celery

This cookiecutter has an optional [Celery](http://www.celeryproject.org/) integration that let you choose if you want to use it or not in your project.
If you choose to use Celery, additionnal code and files will be generated to get started with it.

This code will include a dummy task located in `yourproject/yourapp/tasks/example.py` that only return `"OK"` and a `celery_app` file used to your celery workers.


#### Running celery workers

In your project path, once dependencies are installed, you can just run

```
celery worker -A myapi.celery_app:app --loglevel=info
```

If you have updated your configuration for broker / result backend your workers should start and you should see the example task avaible

```
[tasks]
  . myapi.tasks.example.dummy_task
```


#### Running a task

To run a task you can either import it and call it

```python
>>> from myapi.tasks.example import dummy_task
>>> result = dummy_task.delay()
>>> result.get()
'OK'
```

Or use the celery extension

```python
>>> from myapi.extensions import celery
>>> celery.send_task('myapi.tasks.example.dummy_task').get()
'OK'
```

## Using docker

**WARNING** both Dockerfile and `docker-compose.yml` are **NOT** suited for production, use them for development only or as a starting point.

This template offer simple docker support to help you get started and it comes with both Dockerfile and a `docker-compose.yml`. Please note that docker-compose is mostly useful when using celery
since it takes care of running rabbitmq, redis, your web API and celery workers at the same time, but it also work if you don't use celery at all.

Dockerfile has intentionally no entrypoint to allow you to run any command from it (server, shell, init, celery, ...)

Note that you still need to init your app on first start, even when using compose.

```bash
docker build -t myapp .
...
docker run --env-file=.flaskenv myapp myapi init
docker run --env-file=.flaskenv -p 5000:5000 myapp myapi run -h 0.0.0.0
 * Serving Flask app "myapi.app:create_app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 214-619-010
```

With compose

```bash
docker-compose up
...
docker exec -it <container_id> myapi init
```

## Changelog

### 22/05/2019

* Updated docker structure for more production ready configuration.
* Removed Auth endpoint in favor of a third party Auth provider, this lease the template to be more extensiable for use as many services within the same application.
* Added option to use Intel python distribution for better data analysis libraries out of the box!

### 26/04/2019

* Added docker and docker-compose support

### 24/04/2019

* Update configuration to only use env variables, `.flaskenv` has been updated too
* Add unit tests for celery
* Add flake8 to tox
* Configuration file cannot be overridden by `MYAPP CONFIG` env variable anymore
* various cleanups (unused imports, removed `configtest.py` file, flake8 errors)

