# Top level that defines the Flask application instance
# imports the application instance

#  Flask application instance is called app(2) and is a member of the app package(1).
from app import app, db
from app.models import User, Post

app.config['SECRET_KEY']
'you-will-never-guess'

# decorator - registers the function as a shell context function. Returns a dictionary and a list because for each item we have to provide a name under which it will be referenced in the shell, given by dictionary keys.
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}