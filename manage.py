"""
manage.py
- provides a command line utility for interacting with the
  application to perform interactive debugging and setup
"""
import click
from flask.cli import FlaskGroup
from flask_migrate import Migrate

from surveyapi.application import create_app
from surveyapi.models import db, Survey, Question, Choice
app = create_app()




cli = FlaskGroup(app)

migrate = Migrate(app, db)

# manager = Manager(app)

migrate = Migrate()
migrate.init_app(app, db)

# provide a migration utility command
# manager.add_command('db', MigrateCommand)

# enable python shell with application context
@cli.command('test')
@click.argument('test_case', default='test*.py')
def test(test_case='test*.py'):
  pass


if __name__ == "__main__":
    cli()