from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, NumberRange

class BraceletForm(FlaskForm):
    name = StringField('Bracelet Name', validators=[DataRequired()])
    price = FloatField('Price ($)', validators=[DataRequired(), NumberRange(min=0)])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Add / Update Bracelet')

class OrderForm(FlaskForm):
    buyer_name = StringField("Your Name", validators=[DataRequired()])
    student_name = StringField("Student's Name", validators=[DataRequired()])
    grade = SelectField("Grade", choices=[('6', '6th Grade'), ('7', '7th Grade'), ('8', '8th Grade')], validators=[DataRequired()])
    bracelet_id = SelectField("Bracelet", coerce=int, validators=[DataRequired()])
    quantity = IntegerField("Quantity", validators=[DataRequired(), NumberRange(min=1)])
    payment_note = TextAreaField("Payment Method / Notes")
    submit = SubmitField("Place Order")

