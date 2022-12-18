from flask import Blueprint, render_template, redirect, url_for, redirect, flash
from expense_tracker.forms import RegistrationForm, LoginForm, ExpenseForm
from .extensions import db, bcrypt
from expense_tracker.models import User, Expenses
from flask_login import login_user, current_user, logout_user
from datetime import date, timedelta, datetime
import json
from pprint import pprint
from sqlalchemy import func
from sqlalchemy import text
from .helper_functions import create_expenses_chart, create_expense_summary, get_recent_expenses

views = Blueprint("views",__name__)

dummy_expenses = [
    {
        "name": "Example 1",
        "category": "Rent",
        "amount": 1000,
        "date": date(2022,1,1)
    },
    {
        "name": "Example 2",
        "category": "Other",
        "amount": 1000,
        "date": date(2022,2,2)
    },
    {
        "name": "Example 3",
        "category": "Food",
        "amount": 1000,
        "date": date(2022,3,3)
    }
]



@views.route("/", methods = ["GET", "POST"])
def home():
    form = ExpenseForm()   
    expense_categories = form.category.choices

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
        
        
        # summary = {"category": [],
        #             "expense_sum": []}
        # for item in expense_categories:
        #     # Query returns a list of touples, [0][0] gets the actual number 
        #     # "or 0" at the end means result is 0 if query returns <None>. 
        #     result = db.session.query(func.sum(Expenses.amount).label('category_sum')).filter_by(
        #         category=item, user_id=current_user.id).all()[0][0] or 0

        #     summary["category"].append(item)
        #     summary["expense_sum"].append(result)

        summary = create_expense_summary(expense_categories)
        graphJSON = create_expenses_chart(summary=summary, title="Your Expense Summary (Past 30 Days)")

        # recent_expenses = {}
       
        # recent_expenses["past_week"] = db.session.query(func.sum(Expenses.amount).label('weekly_spendings')).filter(
        #     Expenses.date >= datetime.now() - timedelta(weeks=1), Expenses.user_id == current_user.id).all()[0][0] or 0

        # recent_expenses["past_month"] = db.session.query(func.sum(Expenses.amount).label('weekly_spendings')).filter(
        #     Expenses.date >= datetime.now() - timedelta(days=30), Expenses.user_id == current_user.id).all()[0][0] or 0

        # recent_expenses["past_year"] = db.session.query(func.sum(Expenses.amount).label('weekly_spendings')).filter(
        #     Expenses.date >= datetime.now() - timedelta(days=365), Expenses.user_id == current_user.id).all()[0][0] or 0

        recent_expenses = get_recent_expenses()

        

        return render_template("home.html", expenses= user_expenses, form=form, graphJSON=graphJSON, recent_expenses=recent_expenses)
    else:
        
        # example_summary = {"category": expense_categories,
        #             "expense_sum": [1000 for i in expense_categories]}

        example_summary = {}
        for item in expense_categories:
            example_summary[item] = 1000
        
        graphJSON = create_expenses_chart(summary=example_summary, title="Example Expenses Chart")
        example_recent_expenses = {
            "past_week": 0,
            "past_month": 0,
            "past_year": 0
        }       
           
        return render_template("home.html", expenses=dummy_expenses, form=form, graphJSON=graphJSON, recent_expenses=example_recent_expenses)


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

@views.route("/expenses/delete/<int:id>", methods=["POST"])
def delete_expense(id):
    expense_to_delte = Expenses.query.get_or_404(id)

    try:
        db.session.delete(expense_to_delte)
        db.session.commit()

        print("-"*100)
        print(f"need to delete expense: ID - {expense_to_delte.id} | NAME - {expense_to_delte.name}")
        print("-"*100)


        flash("Expense deleted","success")
        return redirect(url_for("views.home"))

    except:
        flash("There was an error deleting that expense, please try again","danger")
        return redirect(url_for("views.home"))

