from Models.models import Receipt as ReceiptModel
from flask import Blueprint, request, jsonify
from Services.receipt_processor import preprocess_image, process_receipt
from responses.factory.Success import Success
from responses.factory.Error import Error
from datetime import datetime
from uuid import UUID

routes = Blueprint("routes", __name__)

BASED_URL = "/api/"

# url: http://127.0.0.1:5001/api/extract_receipts
@routes.route(BASED_URL + "initx", methods=["GET"])
def initx():
    return Success("Init System! - 200 OK").json_respond()

@routes.route(BASED_URL + "receipts", methods=["GET"])
def all_receipts():
    """Get all receipts"""
    receipts = ReceiptModel.query.all()
    return Success(None, {receipt.id: receipt.to_dict() for receipt in receipts})

@routes.route(BASED_URL + "extract_receipts", methods=["POST"])
def extract_receipts():
    """Extract receipts from image"""
    if "receipts" not in request.files:
        return jsonify({"error": "No file part"}), 400
    # receipts_objects = request.files['receipts']
    receipts_objects = request.files.getlist("receipts")
    processed_image = process_receipt(receipts_objects)
    # processed_image = preprocess_image(receipts_objects)
    if processed_image is None:
        return Error("Image processing failed").json_respond()
    return Success("Image processed successfully", processed_image).json_respond()

@routes.route(BASED_URL + "save_receipts", methods=["Post"])
def save_receipts():
    """Save multiple receipts"""
    mutiple_receipt = request.json
    is_valid, message = ReceiptModel.save_many(mutiple_receipt)
    return is_valid and Success(message).json_respond() or Error(message).json_respond()

@routes.route(BASED_URL + "receipt/<uuid:id>", methods=["GET"])
def get_receipt():
    """Get a receipt by id"""
    receipt = ReceiptModel.query.get_or_404(id)
    return Success(None, {receipt.id: receipt.to_dict()})

@routes.route(BASED_URL + "receipts", methods=["POST"])
def edit_receipts():
    """Update multiple receipts"""
    mutiple_receipt = request.json
    is_valid, message = ReceiptModel.edit_many(mutiple_receipt)
    return is_valid and Success(message).json_respond() or Error(message).json_respond()
