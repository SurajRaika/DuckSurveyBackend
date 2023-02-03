import os
from surveyapi.application import create_app
from surveyapi.models import db, Survey, Question, Choice 
from flask_migrate import Migrate

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db,render_as_batch=True)



@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, Survey=Survey, Question=Question,
                Choice=Choice)


# use command : $env:FLASK_APP = "flasky.py"
# $env:FLASK_DEBUG = 1 
# for set environment variable
#  