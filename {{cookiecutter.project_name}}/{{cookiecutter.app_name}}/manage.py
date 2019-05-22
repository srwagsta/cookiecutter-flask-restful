import click
from flask.cli import FlaskGroup

from {{cookiecutter.app_name}}.app import create_app


def create_{{cookiecutter.app_name}}(info):
    return create_app(cli=True)


@click.group(cls=FlaskGroup, create_app=create_{{cookiecutter.app_name}})
def cli():
    """Main entry point"""


@cli.command("init")
def init():
    """Init application, create database tables
    and create a new user named admin with password admin
    """
    from {{cookiecutter.app_name}}.extensions import db
    click.echo("create database")
    db.create_all()
    click.echo("done")


@cli.command("create-example")
def create_example():
    from {{cookiecutter.app_name}}.models import Example
    click.echo("create example entry")
    entry = Example(
        name='test-entry'
    )
    db.session.add(entry)
    db.session.commit()
    click.echo("created test example entry")

if __name__ == "__main__":
    cli()
