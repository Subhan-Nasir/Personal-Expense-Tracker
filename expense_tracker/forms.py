from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DecimalField, DateField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from expense_tracker.models import User


class RegistrationForm(FlaskForm):

    username = StringField("Username", validators=[
                           DataRequired(), Length(2, 25)])
    email = StringField("Email", validators=[DataRequired(), Email()])

    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[
                                     DataRequired(), EqualTo("password", message="Passwords don't match")])

    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError(
                "Username already exists. Please choose a different one.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError(
                "Email already exists. Please choose a different one.")


class LoginForm(FlaskForm):

    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])

    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class ExpenseForm(FlaskForm):

    name = StringField("Name", validators=[DataRequired()])
    # category = StringField("Category", validators=[DataRequired()])

    category = SelectField("Category", choices=["Rent", "Food", "Other"], default="Other",validators=[DataRequired()])

    amount = DecimalField("Amount", validators=[DataRequired(), NumberRange(
        min=0, message="Cannot enter negative numbers")])
    date = DateField("Date", format='%Y-%m-%d', validators=[DataRequired()])

    submit = SubmitField("Save")


