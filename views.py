from flask import Blueprint, render_template, redirect, url_for, redirect, flash
from forms import RegistrationForm, LoginForm


views = Blueprint(__name__, "views")

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

    form = RegistrationForm()

    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}.", "success")
        print("LOGIN SUCCESSFUL")
        return redirect(url_for("views.home"))
    else:
        return render_template("register.html", title="Register", form = form)



@views.route("/login", methods = ["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        if form.email.data == "admin@gmail.com" and form.password.data == "admin":
            flash("Login successful", "success")
            return(redirect(url_for("views.home")))
        else:
            flash("Uncessful login. Check details and try again", "danger")

    return render_template("login.html", title = "Login", form = form)
