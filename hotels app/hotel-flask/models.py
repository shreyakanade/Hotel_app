from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    room_no = db.Column(db.Integer, nullable=False)
    guests = db.Column(db.Integer, default=1)
    check_in = db.Column(db.Date, nullable=False)
    check_out = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(30), default="booked")  # booked, checked_in, checked_out
    package_id = db.Column(db.Integer, db.ForeignKey('package.id'), nullable=True)
    package = db.relationship("Package", backref="bookings")
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    actual_checkin = db.Column(db.DateTime, nullable=True)
    actual_checkout = db.Column(db.DateTime, nullable=True)

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
