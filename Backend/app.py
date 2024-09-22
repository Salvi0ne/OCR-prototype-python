import os
from flask import Flask
from Models.models import db
from flask_cors import CORS
from dotenv import load_dotenv
from Routes.routes import routes

load_dotenv()

app = Flask(__name__)
app.debug = True

CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db.init_app(app)

app.register_blueprint(routes)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        output = []
    for rule in app.url_map.iter_rules():
        methods = ", ".join(rule.methods)
        route = f"{rule.endpoint}: {rule} ({methods})"
        output.append(route)
    print("----------Route:List----------------")
    for line in sorted(output):
        print(line)
    print("------------------------------------")
    app.run(host="0.0.0.0", port=5001, debug=True)
