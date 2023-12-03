import dash
from dash import dcc, html, Input, Output, dash_table
import pandas as pd

# Initialize the Dash app
app = dash.Dash(__name__)

df = pd.read_csv('data/portal.csv')

# Unique list of schools
schools = df['origin'].dropna().unique().tolist() + df['destination'].dropna().unique().tolist()
schools = list(set([school for school in schools if school]))  # Removing duplicates and None

app.layout = html.Div([
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

    # Table for 'Who is Coming'
    html.Div(
        [html.H3("Who is Coming"),
        dash_table.DataTable(id='joining-players-table')],
        style={'width': '75%', 'margin': '10px'}
    ),

    # Table for 'Who is Leaving'
    html.Div(
        [html.H3("Who is Leaving"),
        dash_table.DataTable(id='leaving-players-table')],
        style={'width': '75%', 'margin': '10px'}
    ),

    # Table for 'Average Ratings and Stars'
    html.Div(
        [html.H3("Average Ratings and Stars"),
        dash_table.DataTable(id='avg-ratings-table')],
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
    df_leaving = df[(df['origin'] == selected_school) & (df['season'] == 2023)].sort_values(by='stars', ascending=False)
    df_joining = df[(df['destination'] == selected_school) & (df['season'] == 2023)].sort_values(by='stars', ascending=False)

    # Prepare data for the player tables
    table_data_leaving = df_leaving[['first_name', 'last_name', 'destination', 'rating', 'stars']].to_dict('records')
    columns_leaving = [{"name": i, "id": i} for i in df_leaving[['first_name', 'last_name', 'destination', 'rating', 'stars']].columns]

    table_data_joining = df_joining[['first_name', 'last_name', 'origin', 'rating', 'stars']].to_dict('records')
    columns_joining = [{"name": i, "id": i} for i in df_joining[['first_name', 'last_name', 'origin', 'rating', 'stars']].columns]

    # Calculate average ratings and stars
    avg_rating_leaving = df_leaving['rating'].mean()
    avg_stars_leaving = df_leaving['stars'].mean()
    avg_rating_joining = df_joining['rating'].mean()
    avg_stars_joining = df_joining['stars'].mean()

    # Calculate rating and star scores
    rating_score = avg_rating_joining / avg_rating_leaving if avg_rating_leaving else None
    star_score = avg_stars_joining / avg_stars_leaving if avg_stars_leaving else None

    # Prepare data for the average ratings and stars table
    avg_ratings_data = [
        {
            'Method': 'Rating',
            'Avg Leaving': avg_rating_leaving,
            'Avg Joining': avg_rating_joining,
            'Score': rating_score
        },
        {
            'Method': 'Stars',
            'Avg Leaving': avg_stars_leaving,
            'Avg Joining': avg_stars_joining,
            'Score': star_score
        }
    ]
    avg_ratings_columns = [{"name": i, "id": i} for i in ['Method', 'Avg Leaving', 'Avg Joining', 'Score']]

    return table_data_leaving, columns_leaving, table_data_joining, columns_joining, avg_ratings_data, avg_ratings_columns

if __name__ == '__main__':
    app.run_server(debug=True, port=8052)
