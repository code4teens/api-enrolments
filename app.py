from flask import Flask

from api_enrolments import api_enrolments
from database import db_session

app = Flask(__name__)
app.register_blueprint(api_enrolments)


@app.teardown_appcontext
def close_session(exception=None):
    db_session.remove()
