from app.extensions import db

class Staff(db.Model):


    # create the database info
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True, unique=True)

    active = db.Column(db.Boolean, nullable=False, default=True)

    # this doesn't actually create a python object, it creates a python level relationship with the user object
    # so we don't have to keep on manually looking up data in the database
    # rather than doing loads of queries, we can access it by saying staff.user
    # the foreign key defines the database link, db.relationship defines how we navigate that link
    # using python
    # remember the database creation is separate from the python object creation


    user = db.relationship('User', back_populates='staff')

    working_hours = db.relationship('WorkingHours', back_populates='staff')

    unavailable_periods = db.relationship('UnavailablePeriod', back_populates='staff')

    bookings = db.relationship('Booking', back_populates='staff')
