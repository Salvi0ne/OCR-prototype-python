from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import traceback
from dotenv import load_dotenv
import openai
import logging
from flask_cors import CORS
from functools import wraps

logging.basicConfig(level=logging.DEBUG)

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

openai.api_key = os.getenv("OPENAI_API_KEY")

SECURITY_KEY = os.getenv("SECURITY_KEY", "123456789qwertyuiop")

def require_security_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        provided_key = request.headers.get('Security-Key')
        if provided_key and provided_key == SECURITY_KEY:
            return f(*args, **kwargs)
        else:
            return jsonify({"error": "Invalid or missing security key"}), 401
    return decorated

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
@require_security_key
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
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/receipts', methods=['GET'])
@require_security_key
def get_receipts():
    receipts = Receipt.query.all()
    return jsonify({receipt.id: receipt.to_dict() for receipt in receipts})

@app.route('/receipts/<int:receipt_id>', methods=['GET'])
@require_security_key
def get_receipt(receipt_id):
    receipt = Receipt.query.get_or_404(receipt_id)
    return jsonify({receipt_id: receipt.to_dict()})

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/parse_receipt', methods=['POST'])
@require_security_key
def parse_receipt():
    text = request.json.get('text', '')
    if not text:
        return jsonify({"error": "No text provided"}), 400
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a receipt parser. Extract the date, total amount, and category."},
                {"role": "user", "content": f"Parse this receipt: {text}"}
            ]
        )
        parsed_data = response.choices[0].message['content']
        return jsonify({"response": parsed_data})
    except Exception as e:
        app.logger.error(f"Error in parse_receipt: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5001, debug=True)
