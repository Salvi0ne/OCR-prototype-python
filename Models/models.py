from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Receipt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)
    date_updated = db.Column(db.DateTime, nullable=False)

    def to_dict(self):
        return {
            "date": self.date.isoformat(),
            "category": self.category,
            "total": self.total,
        }

    def __repr__(self):
        return f"<Receipt {self.id}, {self.date}, {self.category}, {self.total}>"

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return True