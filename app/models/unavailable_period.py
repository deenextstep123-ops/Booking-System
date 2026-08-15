from app.extensions import db


class UnavailablePeriod(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    # Staff can give a reason as to why a period is unavailable, e.g. holiday
    # by setting nullable to true, they don't have to enter a reason, it will just be null
    reason = db.Column(db.String(200), nullable=True)

    staff = db.relationship('Staff', back_populates='unavailable_periods')


