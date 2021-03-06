from os import getenv
from app import create_app

app = create_app(getenv("FLASK_ENV"))


@app.shell_context_processor
def make_shell_context():
    return globals()
