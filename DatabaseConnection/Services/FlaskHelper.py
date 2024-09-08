from DatabaseConnection.Services.FlaskWrapper import FlaskWrapper
import sys

def flask_init_setup():
    flask = FlaskWrapper()
    if not flask.validate_db_connection():
        print("Failed to connect to the database. Please check your connection settings.")
        sys.exit()
    return flask
