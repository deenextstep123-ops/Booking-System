from app.extensions import db

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    duration_minutes = db.Column(db.Integer, nullable=False)

    bookings = db.relationship('Booking', back_populates='service')