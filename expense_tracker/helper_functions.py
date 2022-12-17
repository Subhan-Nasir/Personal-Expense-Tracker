
import pandas as pd
import plotly
import plotly.express as px
import json

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
    df = pd.DataFrame(summary)

    fig = px.pie(df, names="category", values="expense_sum", hole=0.5)
        
    fig.update_traces(textposition='inside', 
        text=df['expense_sum'].map("£{:.2f}".format),
        textinfo='percent+text',
        
        hovertemplate="</br><b>%{label}</b> </br> £%{value:.2f}, </br> %{percent:.2f}"
    )

    fig.add_annotation(
        x= 0.5,
        y = 0.5,
        text = "<b>£{:,.2f}<b>".format(sum(summary["expense_sum"])),                    
        showarrow = False
    )

    fig.update_layout(title_text=f"<b>{title}<b>", title_x = 0.9)
    fig.update_traces(insidetextorientation='horizontal')
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5
    ))

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


if __name__ == "__main__":
    pass
