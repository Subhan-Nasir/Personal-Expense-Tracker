from flask import Blueprint, render_template, redirect, url_for, redirect, flash
from expense_tracker.forms import RegistrationForm, LoginForm, ExpenseForm
from .extensions import db, bcrypt
from expense_tracker.models import User, Expenses
from flask_login import login_user, current_user, logout_user
import datetime

views = Blueprint("views",__name__)

dummy_expenses = [
    {
        "name": "Example 1",
        "category": "Rent",
        "amount": 1000,
        "date": datetime.date(2022,1,1)
    },
    {
        "name": "Example 2",
        "category": "Other",
        "amount": 200,
        "date": datetime.date(2022,2,2)
    },
    {
        "name": "Example 3",
        "category": "Food",
        "amount": 100,
        "date": datetime.date(2022,3,3)
    }
]


@views.route("/", methods = ["GET", "POST"])
def home():
    form = ExpenseForm()

    if form.validate_on_submit():
        print("-"*50)
        print("NEW EXPENSE:")
        print(f"{form.name.data} - {form.category.data} - {form.amount.data} - {form.date.data}")
        print("-"*50)

        new_expense = Expenses(
            name=form.name.data,
            category = form.category.data,
            amount = form.amount.data,
            date = form.date.data,
            user = current_user)

        db.session.add(new_expense)
        db.session.commit()

    if current_user.is_authenticated:
        user_expenses = current_user.expenses
        return render_template("home.html", expenses = user_expenses, form=form)
    else:   
        return render_template("home.html", expenses = dummy_expenses, form=form)


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