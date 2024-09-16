from Models.models import Receipt, db
from flask import Blueprint, request, jsonify
from Routes.middleware import middleware
from Services.receipt_processor import preprocess_image, process_receipt
from responses.factory.Success import Success
from responses.factory.Error import Error
from datetime import datetime

routes = Blueprint("routes", __name__)

BASED_URL = "/api/"

@routes.route("/initx", methods=["GET"])
def initx():
    return Success("Init System! - 200 OK").json_respond()


@routes.route(BASED_URL + "table_receipts", methods=["GET"])
def table_receipts():
    receipts = Receipt.query.all()
    return Success(None, {receipt.id: receipt.to_dict() for receipt in receipts})

# url: http://127.0.0.1:5001/api/extract_receipts
@routes.route(BASED_URL + "extract_receipts", methods=["POST"])
def extract_receipts():
    if "receipts" not in request.files:
        return jsonify({"error": "No file part"}), 400
    # receipts_objects = request.files['receipts']
    receipts_objects = request.files.getlist("receipts")
    # print(receipts_objects)
    processed_image = process_receipt(receipts_objects)
    # processed_image = preprocess_image(receipts_objects)
    if processed_image is None:
        return Error("Image processing failed").json_respond()
    return Success("Image processed successfully", processed_image).json_respond()

@routes.route(BASED_URL + "save_receipts", methods=["GET"])
def save_receipts():
    data = request.json
    try:
        new_receipt = Receipt(
            date=datetime.fromisoformat(data["date"]),
            category=data["category"],
            total=float(data["total"]),
        )
        new_receipt.save()
        return jsonify({new_receipt.id: new_receipt.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return Error(str(e)).json_respond()

@routes.route(BASED_URL + "receipts", methods=["GET"])
def get_receipts():
    receipts = Receipt.query.all()
    return Success(None, {receipt.id: receipt.to_dict() for receipt in receipts})

@routes.route(BASED_URL + "receipts", methods=["POST"])
def edit_receipts():
    data = request.json
    try:
        receipt = Receipt.query.get_or_404(data["id"])
        receipt.date = data["date"]
        receipt.category = data["category"]
        receipt.total = data["total"]
        receipt.save()
        return Success(None, {receipt.id: receipt.to_dict()}).json_respond()
    except Exception as e:
        return Error(str(e)).json_respond()
