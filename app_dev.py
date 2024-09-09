from DatabaseConnection.Services.FlaskHelper import flask_sqlalchemy
from flask import Flask
from flask_cors import CORS
from Routes.route import main_blueprint

app = Flask(__name__)
CORS(app)
db = flask_sqlalchemy(app)
app.register_blueprint(main_blueprint)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
