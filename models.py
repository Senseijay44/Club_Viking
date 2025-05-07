from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Bracelet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Bracelet {self.name}>'

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    buyer_name = db.Column(db.String(100), nullable=False)
    student_name = db.Column(db.String(100), nullable=False)
    grade = db.Column(db.String(10), nullable=False)
    bracelet_id = db.Column(db.Integer, db.ForeignKey('bracelet.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    payment_note = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    bracelet = db.relationship('Bracelet')

    def __repr__(self):
        return f'<Order {self.id}>'

