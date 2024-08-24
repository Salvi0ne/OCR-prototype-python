from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

app = Flask(__name__)

# PostgreSQL database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

class Receipt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    total = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'date': self.date.isoformat(),
            'category': self.category,
            'total': self.total
        }

@app.route('/receipts', methods=['POST'])
def add_receipt():
    data = request.json
    try:
        new_receipt = Receipt(
            date=datetime.fromisoformat(data['date']),
            category=data['category'],
            total=float(data['total'])
        )
        db.session.add(new_receipt)
        db.session.commit()
        return jsonify({new_receipt.id: new_receipt.to_dict()}), 201
    except KeyError as e:
        return jsonify({'error': f'Missing required field: {str(e)}'}), 400
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/receipts', methods=['GET'])
def get_receipts():
    receipts = Receipt.query.all()
    return jsonify({receipt.id: receipt.to_dict() for receipt in receipts})

@app.route('/receipts/<int:receipt_id>', methods=['GET'])
def get_receipt(receipt_id):
    receipt = Receipt.query.get_or_404(receipt_id)
    return jsonify({receipt_id: receipt.to_dict()})

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)