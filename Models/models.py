from functools import wraps
import uuid
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from datetime import datetime

db = SQLAlchemy()

class Receipt(db.Model):
    id = db.Column(db.Uuid, primary_key=True, default=uuid.uuid4)
    total = db.Column(db.Float, nullable=True, default=0.0)
    category = db.Column(db.String(100), nullable=True)
    date = db.Column(db.DateTime, nullable=True)
    date_created = db.Column(db.DateTime, nullable=True)
    date_updated = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        """Return a dictionary representation of the Receipt object."""
        return {
            "date": self.date.isoformat() if self.date else None,
            "category": self.category,
            "total": self.total,
        }

    def __repr__(self):
        return f"<Receipt {self.id}, {self.date}, {self.category}, {self.total}>"

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True, self
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True, "Receipt deleted successfully"
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    @staticmethod
    def save_many(self, mutiple_receipt):
        try:
            is_valid, message = Receipt.save_many_validator(mutiple_receipt)
            if not is_valid:
                return False, message

            new_receipts = []
            for receipt_data in mutiple_receipt:
                new_receipt = Receipt(
                    date=datetime.fromisoformat(receipt_data["date"]),
                    category=receipt_data["category"],
                    total=float(receipt_data["total"]),
                    date_created=datetime.now(),
                )
                new_receipts.append(new_receipt)
            db.session.bulk_insert_mappings(
                Receipt, [receipt.to_dict() for receipt in new_receipts]
            )
            db.session.commit()
            return True, "Receipts saved successfully"
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    @staticmethod
    def edit_many(mutiple_receipt):
        try:
            is_valid, message = Receipt.edit_many_validator(mutiple_receipt)
            if not is_valid:
                return is_valid, message

            for receipt_data in mutiple_receipt:
                receipt = Receipt.query.get(receipt_data["id"])
                receipt.date = datetime.fromisoformat(receipt_data["date"])
                receipt.category = receipt_data["category"]
                receipt.total = float(receipt_data["total"])
                receipt.date_updated = datetime.now()
                db.session.add(receipt)
            db.session.commit()
            return True, "Receipts edited successfully"
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    @staticmethod
    def save_many_validator(mutiple_receipt):
        for receipt_data in mutiple_receipt:
            is_valid, error_message = Receipt.validate_receipt_data(receipt_data)
            if not is_valid:
                return False, error_message
        return True, None

    @staticmethod
    def edit_many_validator(mutiple_receipt):
        for receipt_data in mutiple_receipt:
            is_valid, error_message = Receipt.validate_receipt_data(receipt_data)
            if not is_valid:
                return False, error_message

            if Receipt.get_receipt_by_id(receipt_data["id"]) is None:
                return (
                    False,
                    f"Receipt with ID {receipt_data['id']} does not exist, Edit operation failed",
                )
        return True, None

    @staticmethod
    def get_receipt_by_id(id):
        receipt = Receipt.query.get(id)
        return receipt

    @staticmethod
    def validate_receipt_data(receipt):
        if "date" not in receipt or "category" not in receipt or "total" not in receipt:
            return False, "Missing required fields: id, date, category, total"
        try:
            datetime.fromisoformat(receipt["date"])
        except ValueError:
            return False, "Invalid date format"
        try:
            float(receipt["total"])
        except ValueError:
            return False, "Invalid total format"
        if not isinstance(receipt["category"], str):
            return False, "Invalid category format"

        return True, None
