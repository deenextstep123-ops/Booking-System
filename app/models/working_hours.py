
from app.extensions import db

class WorkingHours(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
        day_of_week = db.Column(db.Integer, nullable=False)
        start_time = db.Column(db.Time, nullable=False)
        end_time = db.Column(db.Time, nullable=False)


        # same again, by creating a relationship between the staff and working hours databases,
        # this creates a python level relationship so we can use staff.working_hours and working_hours.staff
        # rather than having to manually query the database
        staff = db.relationship('Staff', back_populates='working_hours')