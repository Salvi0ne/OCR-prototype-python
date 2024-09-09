import unittest
from DatabaseConnection.Services.FlaskHelper import flask_sqlalchemy
from flask import Flask
from flask_cors import CORS
from sqlalchemy import text

app = Flask(__name__)
db = flask_sqlalchemy(app)

class TestConnectToDatabase(unittest.TestCase):
    def test_connect_to_database_posgres(self):
        with app.app_context():
            flag = False
            try:
                with app.app_context():
                    db.session.execute(text("SELECT 1"))
                    flag = True
            except Exception as e:
                print(f"Error: {e}")    
            self.assertTrue(flag)

if __name__ == '__main__':
    unittest.main()
