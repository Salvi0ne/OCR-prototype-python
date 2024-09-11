from flask import Blueprint, request
from Routes.middleware import auth_middleware

main_blueprint = Blueprint("main", __name__)

@main_blueprint.route("/initx", methods=["GET"])
def initx():
    return "Init System! - 200 OK"

@main_blueprint.route("/receipts", methods=["POST"])
@auth_middleware
def receipts():
    #...
    pass 
