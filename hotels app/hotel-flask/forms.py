from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SelectField, SubmitField, FloatField, TextAreaField
from wtforms.validators import DataRequired, Length

class BookingForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=120)])
    phone = StringField("Phone", validators=[DataRequired(), Length(max=30)])
    room_no = IntegerField("Room Number", validators=[DataRequired()])
    guests = IntegerField("Number of Guests", default=1)
    check_in = DateField("Check-in Date", validators=[DataRequired()], format="%Y-%m-%d")
    check_out = DateField("Check-out Date", validators=[DataRequired()], format="%Y-%m-%d")
    package = SelectField("Package", coerce=int, choices=[(0,"None")])
    submit = SubmitField("Book")

class MenuForm(FlaskForm):
    name = StringField("Dish name", validators=[DataRequired()])
    price = FloatField("Price", validators=[DataRequired()])
    description = TextAreaField("Description")
    submit = SubmitField("Add")
