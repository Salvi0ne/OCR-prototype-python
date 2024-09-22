from Models.models import Receipt as ReceiptModel
from flask import Blueprint, request, jsonify, send_file
from Services.receipt_processor import process_list_of_receipts, process_receipt
from responses.factory.Success import Success
from responses.factory.Error import Error
from datetime import datetime
from uuid import UUID
from icecream import ic
import json
import pandas as pd
import io

routes = Blueprint("routes", __name__)

BASED_URL = "/api/"


# url: http://127.0.0.1:5001/api/extract_receipts
@routes.route(BASED_URL + "initx", methods=["GET"])
def initx():
    return Success("Init System! - 200 OK").json_respond()


@routes.route(BASED_URL + "receipts/<string:status>", methods=["GET"])
def all_receipts(status: str):
    """Get all receipts based on status"""
    if status not in ["verified", "unverified"]:
        return Error(
            "Invalid status. Only 'verified' and 'unverified' are allowed."
        ).json_respond()
    receipts = ReceiptModel.query.filter_by(status=status).all()
    if not receipts:
        return Success("No receipts found with the given status.", {}).json_respond()
    receipts_dict = [receipt.to_dict() for receipt in receipts]
    return Success("Retrieved Receipts status: " + status, receipts_dict).json_respond()


@routes.route(BASED_URL + "extract_receipts", methods=["POST"])
def extract_receipts():
    """Extract receipts from image"""
    # ic(request.files);
    receipts_objects = request.files.getlist("files")
    if "files" not in request.files:
        return jsonify({"error": "No file part"}), 400
    # ic(receipts_objects);
    processed_images = process_list_of_receipts(receipts_objects)
    # return Success("Images processed successfully").json_respond()
    if processed_images is None:
        return Error("Failed to process images").json_respond()
    [is_save, message] = ReceiptModel.save_many(processed_images)
    if is_save is False:
        return Error(message).json_respond()
    return Success("Images processed successfully").json_respond()

@routes.route(BASED_URL + "save_receipts", methods=["Post"])
def save_receipts():
    """Save multiple receipts"""
    mutiple_receipt = request.json
    is_valid, message = ReceiptModel.save_many(mutiple_receipt)
    return is_valid and Success(message).json_respond() or Error(message).json_respond()


@routes.route(BASED_URL + "receipt/<uuid:id>", methods=["GET"])
def get_receipt(id):
    """Get a receipt by id"""
    receipt = ReceiptModel.query.get_or_404(id)
    return Success(None, {receipt.id: receipt.to_dict()})


@routes.route(BASED_URL + "receipts", methods=["POST"])
def edit_receipts():
    """Update multiple receipts"""
    mutiple_receipt = request.json
    is_valid, message = ReceiptModel.edit_many(mutiple_receipt)
    return is_valid and Success(message).json_respond() or Error(message).json_respond()


@routes.route(BASED_URL + "get-data-excel", methods=["GET"])
def get_data_excel():
    """Return DataFrame as an Excel file"""
    data = {
        "employees": [
            {"id": 1, "name": "John Doe", "department": "HR", "salary": 50000},
            {"id": 2, "name": "Jane Smith", "department": "Finance", "salary": 60000},
            {"id": 3, "name": "Michael Johnson", "department": "IT", "salary": 75000},
        ]
    }
    df = pd.DataFrame(data["employees"])
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    output.seek(0)
    return send_file(
        output,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        download_name="employees.xlsx",
    )
    # attachment_filename="employees.xlsx",

@routes.route( BASED_URL+"receipt/<uuid:id>", methods=["PATCH"])
def edit_receipt(id):
    """Edit Receipt"""
    # ic(request.json)
    is_valid, message  = ReceiptModel.edit( request.json )
    return is_valid and Success(message).json_respond() or Error(message).json_respond()

@routes.route( BASED_URL+"submit_receipts_to_verify", methods=["POST"])
def submit_receipts_to_verify():
    """Get The Id of Receipts To Verify"""
    id_array = request.json['ids'];
    is_valid, message  = ReceiptModel.submit_receipts_to_verify(id_array)
    return is_valid and Success(message).json_respond() or Error(message).json_respond()

@routes.route( BASED_URL+"receipt/<uuid:id>", methods=["DELETE"])
def delete_receipt(id):
    receipt = ReceiptModel.query.get(id)
    if not receipt: return False, "Receipt not found"
    is_valid, message  = receipt.delete()
    return is_valid and Success(message).json_respond() or Error(message).json_respond()

# @routes.route( "/xx", methods=["POST"])
# def xx():
#     """!!!!xxx!!!!!"""
#     if "files" not in request.files:
#         return jsonify({"error": "No file part"}), 400
#     ic(request.files['files'])
#     return Success("OK").json_respond()
