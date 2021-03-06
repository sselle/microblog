from app import app, db
from app.models import User, Post

# make context available to flask shell
# this is only needed for tests during dev
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}