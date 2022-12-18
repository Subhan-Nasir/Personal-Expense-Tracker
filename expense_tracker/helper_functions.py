
import pandas as pd
import plotly
import plotly.express as px
import json
from expense_tracker.forms import RegistrationForm, LoginForm, ExpenseForm
from .extensions import db
from sqlalchemy import func
from flask_login import current_user
from expense_tracker.models import User, Expenses
from datetime import date, datetime, timedelta

def create_expense_summary(expense_categories):
    """
    Finds how much the user spent on each category of expenses (Housing, Food etc.).

    Args:
        expense_categories (list): Constains all expense categories as strings.

    Returns:
        summary (dictory): Containts two key, value pairs. 
            The "category" key has a list of strings representing expense types. 
            The "expense_sum" key has a list of numbers representing the money spent on each expense type.

    """    

    # summary = {"category": [],
    #                 "expense_sum": []}

    summary = {}
    for item in expense_categories:
        # Query returns a list of touples, [0][0] gets the actual number 
        # "or 0" at the end means result is 0 if query returns <None>. 
        result = db.session.query(func.sum(Expenses.amount).label('category_sum')).filter(
            Expenses.category == item, 
            Expenses.user_id == current_user.id, 
            Expenses.date >= datetime.now() - timedelta(days=30)).all()[0][0] or 0

        summary[item] = result
        

    return summary



def create_expenses_chart(summary, title):
    """
    Creates and returns a pie chart that summarises the users expenses.

    Args:
        summary (dictionary): Containts two key, value pairs. 
            The "category" key has a list of strings representing expense types. 
            The "expense_sum" key has a list of numbers representing the money spent on each expense type.

        title (string): The title of the chart              

    Returns:
        graphJSON: A plotly graph converted to JSON format.
            
    
    """    
    
    
    # df = pd.DataFrame(summary)
    df = pd.DataFrame.from_dict(summary, orient="index").reset_index()
    df.columns = ["category", "expense_sum"]

    fig = px.pie(df, names="category", values="expense_sum",
        hole=0.5, color_discrete_sequence=px.colors.sequential.thermal)
        
    fig.update_traces(textposition='inside', 
        text=df['expense_sum'].map("£{:.2f}".format),
        textinfo='percent+text',
        
        hovertemplate="</br><b>%{label}</b> </br> £%{value:.2f}, </br> %{percent:.2f}",
        sort=True,
        direction="clockwise"
    )

    # Total spending across all categories
    fig.add_annotation(
        x= 0.5,
        y = 0.5,
        text = "<b>£{:,.2f}<b>".format(df["expense_sum"].sum()),                    
        showarrow = False
    )

    fig.update_layout(title_text=f"<b>{title}<b>", title_x = 0.5)
    fig.update_traces(insidetextorientation='horizontal')
    # fig.update_layout(legend=dict(
    #     orientation="h",
    #     yanchor="bottom",
    #     y=-0.25,
    #     xanchor="center",
    #     x=0.5
    # ))

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


def get_recent_expenses():
    """
    Finds the amount of money a user spent in the past week, month, and year.

    Returns:
        recent_expenses (dict): Contains time periods (past week, month, year) as string keys and 
    """    
    recent_expenses = {}

    # Queries the sum of the "amount" column, filtered by current user and specified dates.
    # Query returns a list of touples, [0][0] gets the actual number 
    # "or 0" at the end means result is 0 if query returns <None>.    
    recent_expenses["past_week"] = db.session.query(func.sum(Expenses.amount).label('weekly_spendings')).filter(
        Expenses.date >= datetime.now() - timedelta(weeks=1), Expenses.user_id == current_user.id).all()[0][0] or 0

    recent_expenses["past_month"] = db.session.query(func.sum(Expenses.amount).label('weekly_spendings')).filter(
        Expenses.date >= datetime.now() - timedelta(days=30), Expenses.user_id == current_user.id).all()[0][0] or 0

    recent_expenses["past_year"] = db.session.query(func.sum(Expenses.amount).label('weekly_spendings')).filter(
        Expenses.date >= datetime.now() - timedelta(days=365), Expenses.user_id == current_user.id).all()[0][0] or 0

    return recent_expenses


if __name__ == "__main__":
    pass
