from flask import Blueprint, render_template, redirect, url_for, redirect, flash
from expense_tracker.forms import RegistrationForm, LoginForm
from .extensions import db, bcrypt
from expense_tracker.models import User, Expenses
from flask_login import login_user, current_user, logout_user

views = Blueprint("views",__name__)

expenses = [
    {
        "name": "Rent",
        "amount": 1000,
        "date": "1/1/22"
    },
    {
        "name": "Electricity",
        "amount": 200,
        "date": "2/2/22"
    },
    {
        "name": "Fuel",
        "amount": 100,
        "date": "3/3/22"
    }
]


@views.route("/")
def home():
    return render_template("home.html", expenses = expenses)


@views.route("/about")
def about():
    return render_template("about.html")


@views.route("/go-to-home")
def go_to_home():
    return redirect(url_for("views.home"))


@views.route("/register", methods = ["GET", "POST"])
def register():
    if current_user.is_authenticated: 
        return redirect(url_for("views.home"))
    

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")

        new_user = User(username=form.username.data,
                    email=form.email.data,
                    password=hashed_password)

        db.session.add(new_user)
        db.session.commit()


        flash(f"Account created for {form.username.data}.", "success")
        login_user(new_user)
        print("LOGIN SUCCESSFUL")
        return redirect(url_for("views.home"))
    else:
        return render_template("register.html", title="Register", form = form)



@views.route("/login", methods = ["GET", "POST"])
def login():

    if current_user.is_authenticated: 
        return redirect(url_for("views.home"))

    form = LoginForm()


    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("views.home"))
        else:
            flash("Uncessful login. Check details and try again", "danger")

    return render_template("login.html", title = "Login", form = form)


@views.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("views.home"))