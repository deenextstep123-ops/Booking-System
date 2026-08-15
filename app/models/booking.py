from datetime import datetime, UTC

from app.extensions import db
from enum import Enum

class BookingStatus(Enum):
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    CANCELLED = 'cancelled'
    COMPLETED = 'completed'

class Booking(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)

    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    status = db.Column(db.Enum(BookingStatus), nullable=False, default=BookingStatus.PENDING)

    # it would've been default=datetime.utcnow , but that's deprecated so instead we use
    # datetime.now(UTC), however we need to use lambda: datetime.now()
    # otherwise the time that would be stored would be whatever the time is when the model is imported
    # RATHER THAN when each booking object is created
    # lambda creates a function that returns the current UTC datetime. We pass that function to default
    # so SQLalchemy calls it whenever a new Booking is created, when it needs a new default value
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC))


    staff = db.relationship('Staff', back_populates='bookings')
    service = db.relationship('Service', back_populates='bookings')
    customer = db.relationship('User', back_populates='bookings')
