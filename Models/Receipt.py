from app import db

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
