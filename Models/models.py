from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# class Profile(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(20), unique=False, nullable=False)
#     last_name = db.Column(db.String(20), unique=False, nullable=False)
#     age = db.Column(db.Integer, nullable=False)

#     def __repr__(self):
#         return f"Name: {self.first_name}, Age: {self.age}"

class Receipt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    total = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            'date': self.date.isoformat(),
            'category': self.category,
            'total': self.total
        }

    def __repr__(self):
        return f"<Receipt {self.id}, {self.date}, {self.category}, {self.total}>"
