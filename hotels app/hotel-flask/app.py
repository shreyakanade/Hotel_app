from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from forms import BookingForm, MenuForm
from models import db, Booking, MenuItem, Package
import os
from datetime import datetime

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    db.init_app(app)

    @app.route("/")
    def index():
        total_rooms = 20
        booked = Booking.query.filter(Booking.status != 'checked_out').count()
        return render_template("index.html", total_rooms=total_rooms, booked=booked)

    # Bookings list
    @app.route("/bookings")
    def bookings():
        bookings = Booking.query.order_by(Booking.id.desc()).all()
        return render_template("bookings.html", bookings=bookings)

    # New booking
    @app.route("/booking/new", methods=["GET","POST"])
    def booking_new():
        form = BookingForm()
        packages = Package.query.all()
        form.package.choices = [(0, "None")] + [(p.id, p.name) for p in packages]
        if form.validate_on_submit():
            pkg = form.package.data if form.package.data != 0 else None
            b = Booking(
                name=form.name.data,
                phone=form.phone.data,
                room_no=form.room_no.data,
                guests=form.guests.data,
                check_in=form.check_in.data,
                check_out=form.check_out.data,
                status="booked",
                package_id=pkg
            )
            db.session.add(b)
            db.session.commit()
            flash("Booking created", "success")
            return redirect(url_for("bookings"))
        return render_template("booking_form.html", form=form)

    # Booking detail & check in
    @app.route("/booking/<int:booking_id>")
    def booking_detail(booking_id):
        b = Booking.query.get_or_404(booking_id)
        return render_template("booking_detail.html", b=b)

    # Check-in (changes status)
    @app.route("/booking/<int:booking_id>/checkin", methods=["POST"])
    def booking_checkin(booking_id):
        b = Booking.query.get_or_404(booking_id)
        if b.status == "booked":
            b.status = "checked_in"
            b.actual_checkin = datetime.utcnow()
            db.session.commit()
            flash("Checked in", "success")
        return redirect(url_for("booking_detail", booking_id=booking_id))

    # Checkout
    @app.route("/booking/<int:booking_id>/checkout", methods=["GET","POST"])
    def booking_checkout(booking_id):
        b = Booking.query.get_or_404(booking_id)
        if request.method == "POST":
            b.status = "checked_out"
            b.actual_checkout = datetime.utcnow()
            db.session.commit()
            flash("Checked out", "success")
            return redirect(url_for("bookings"))
        return render_template("checkout.html", b=b)

    # Dinner menu list and add
    @app.route("/menu")
    def menu():
        items = MenuItem.query.all()
        return render_template("menu.html", items=items)

    @app.route("/menu/new", methods=["GET","POST"])
    def menu_new():
        form = MenuForm()
        if form.validate_on_submit():
            item = MenuItem(name=form.name.data, price=form.price.data, description=form.description.data)
            db.session.add(item)
            db.session.commit()
            flash("Menu item added", "success")
            return redirect(url_for("menu"))
        return render_template("menu_form.html", form=form)

    # Packages
    @app.route("/packages")
    def packages():
        packs = Package.query.all()
        return render_template("packages.html", packs=packs)

    return app

# expose app for gunicorn
app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
