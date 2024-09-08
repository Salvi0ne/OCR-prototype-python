
from DatabaseConnection.Services.FlaskHelper import flask_init_setup
from Routes.route import main_blueprint

flask = flask_init_setup()
flask.setup_route_with_blue_print(main_blueprint)

if __name__ == "__main__":
    flask.run_host("0.0.0.0", 5002, debug=True)
