from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import os
from dotenv import load_dotenv

load_dotenv()


class FlaskWrapper:
    def __init__(self):
        self.db = self.connect_database(self)

    @property
    def db(self):
        return self._db

    @db.setter
    def db(self, value):
        self._db = value

    @property
    def app(self):
        return self._app

    @app.setter
    def app(self, value):
        self._app = value

    @staticmethod
    def connect_database(self):
        self.app = Flask(__name__)
        CORS(self.app)
        self.app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db = SQLAlchemy(self.app)
        return db

    def validate_db_connection(self):
        try:
            with self.app.app_context():
                self.db.session.execute(text("SELECT 1"))
                return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def run_host(self, host, port, debug):
        self.app.run(host="0.0.0.0", port=5002, debug=True)
        
    def setup_route_with_blue_print(self, blue_print):
        self.app.register_blueprint(blue_print)

    def __del__(self):
        self.db.session.close()
