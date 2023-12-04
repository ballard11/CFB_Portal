import dash
from dash import dcc, html, Input, Output, dash_table
import pandas as pd

# Initialize the Dash app
app = dash.Dash(__name__)

df = pd.read_csv('data/portal.csv')

# Unique list of schools
schools = df['Origin School'].dropna().unique().tolist() + df['Destination School'].dropna().unique().tolist()
schools = list(set([school for school in schools if school]))  # Removing duplicates and None

app.layout = html.Div([

     html.H3("2023 Transfer Portal - Whose Coming and Going?"),

    # Image container
    html.Div(
        html.Img(src='/assets/Portal.png', width='300px', height='auto')),

    # Dropdown container
    html.Div(
        dcc.Dropdown(
            id='school-dropdown',
            options=[{'label': school, 'value': school} for school in schools],
            value=schools[0],  # Default value
        ),
        style={'width': '25%', 'margin': '10px'}
    ),

    # Table for 'Average Ratings and Stars'
    html.Div(
        [html.H3("Average Ratings and Stars"),
        dash_table.DataTable(id='avg-ratings-table')],
        style={'width': '60%', 'margin': '10px'}
    ),
    
    # Table for 'Who is Coming'
    html.Div(
        [html.H3("Who is Coming?"),
        dash_table.DataTable(id='joining-players-table')],
        style={'width': '75%', 'margin': '10px'}
    ),

    # Table for 'Who is Leaving'
    html.Div(
        [html.H3("Who is Leaving?"),
        dash_table.DataTable(id='leaving-players-table')],
        style={'width': '75%', 'margin': '10px'}
    ),

], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'})


# Callback for updating the tables and average ratings
@app.callback(
    [Output('leaving-players-table', 'data'),
     Output('leaving-players-table', 'columns'),
     Output('joining-players-table', 'data'),
     Output('joining-players-table', 'columns'),
     Output('avg-ratings-table', 'data'),
     Output('avg-ratings-table', 'columns')],
    [Input('school-dropdown', 'value')]
)
def update_tables(selected_school):
    # Filter dataframes for leaving and joining players
    df_leaving = df[(df['Origin School'] == selected_school) & (df['Season'] == 2023)].sort_values(by='Stars', ascending=False)
    df_joining = df[(df['Destination School'] == selected_school) & (df['Season'] == 2023)].sort_values(by='Stars', ascending=False)

    # Prepare data for the player tables
    table_data_leaving = df_leaving[['First Name', 'Last Name', 'Origin School','Destination School', 'Rating', 'Stars']].to_dict('records')
    columns_leaving = [{"name": i, "id": i} for i in df_leaving[['First Name', 'Last Name', 'Origin School','Destination School', 'Rating', 'Stars']].columns]

    table_data_joining = df_joining[['First Name', 'Last Name', 'Origin School', 'Destination School','Rating', 'Stars']].to_dict('records')
    columns_joining = [{"name": i, "id": i} for i in df_joining[['First Name', 'Last Name', 'Origin School', 'Destination School','Rating', 'Stars']].columns]

    # Calculate average ratings and stars
    avg_rating_leaving = df_leaving['Rating'].mean()
    avg_stars_leaving = df_leaving['Stars'].mean()
    avg_rating_joining = df_joining['Rating'].mean()
    avg_stars_joining = df_joining['Stars'].mean()

    # Calculate rating and star scores
    rating_score = avg_rating_joining / avg_rating_leaving if avg_rating_leaving else None
    star_score = avg_stars_joining / avg_stars_leaving if avg_stars_leaving else None

    # Prepare data for the average ratings and stars table
    avg_ratings_data = [
        {
            'Metric': 'Average Joining',
            'Stars': round(avg_stars_joining, 2),
            'Rating': round(avg_rating_joining, 2)
        },
        {
            'Metric': 'Average Leaving',
            'Stars': round(avg_stars_leaving, 2),
            'Rating': round(avg_rating_leaving, 2)
        },
        {
            'Metric': 'Score',
            'Stars': round(star_score, 2) if star_score is not None else None,
            'Rating': round(rating_score, 2) if rating_score is not None else None
        }
    ]

    avg_ratings_columns = [{"name": i, "id": i} for i in ['Metric', 'Stars', 'Rating']]



    return table_data_leaving, columns_leaving, table_data_joining, columns_joining, avg_ratings_data, avg_ratings_columns

if __name__ == '__main__':
    app.run_server(debug=True, port=8080)  # Replace 8080 with any other free port
