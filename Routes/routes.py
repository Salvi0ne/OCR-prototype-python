from flask import Blueprint, request, jsonify
from Routes.middleware import auth_middleware
from responses.factory.Success import Success
# from Models.models import db

routes = Blueprint('routes', __name__)

BASED_URL = "/api/";

@routes.route("/initx", methods=["GET"])
def initx():
    return Success("Init System! - 200 OK").json_respond()

@routes.route(BASED_URL+"table_receipts", methods=["GET"])
@auth_middleware
def table_receipts():
        return "table_receipts! - 200 OK"

# @routes.route(BASED_URL+"save_receipts", methods=["POST"])
# @auth_middleware
# def table_receipts():
#     #...
#     pass

# @routes.route(BASED_URL+"receipts", methods=["GET"])
# @auth_middleware
# def get_receipt():
#     #...
#     pass

# @routes.route(BASED_URL+"receipts", methods=["POST"])
# @auth_middleware
# def post_receipt():
#     pass
