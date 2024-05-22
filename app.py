import dash
from dash import html, dcc, Input, Output
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv('dataset/processed.csv')

# Convert 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')  

# Extract from 'Date' column
df['Month'] = df['Date'].dt.month_name()

# Define months
months = df['Month'].unique()

# Define continents
continents = df['Continent'].unique()

# Define genders
genders = df['Gender'].unique()

# Define sporting events
sporting_events = df['Sport Viewed'].unique()

# Create Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Define CSS styles for buttons
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            .custom-button {
                background-color: #4CAF50; 
                border: none;
                color: white;
                padding: 10px 24px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                margin: 4px 2px;
                transition-duration: 0.4s;
                cursor: pointer;
                border-radius: 8px;
                flex: 1; /* Ensure equal width for buttons */
                max-width: 200px; /* Limit maximum width */
            }

            .custom-button:hover {
                background-color: white;
                color: black;
                border: 2px solid #4CAF50;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Define layout for gender analysis page
gender_layout = html.Div([
    html.H2("Gender-specific Preferences and Behaviours", style={'textAlign': 'center'}),
    
    # Continent selection dropdown
    html.Div([
        html.Label("Select Continent"),
        dcc.Dropdown(
            id='continent-dropdown',
            options=[{'label': continent, 'value': continent} for continent in continents],
            value=continents[0],
            style={'margin-right': '50px', 'font-size': '16px', 'padding': '2px 30px'}  # Added margin-right and increased font size
        ),
    ], style={'display': 'inline-block'}),  # Ensure inline display
    
    # Gender selection dropdown
    html.Div([
        html.Label("Select Gender"),
        dcc.Dropdown(
            id='gender-dropdown',
            options=[{'label': gender, 'value': gender} for gender in genders],
            value=genders[0],
            style={'margin-right': '30px', 'font-size': '16px', 'padding': '2px 15px'}  # Added margin-right and increased font size
        ),
    ], style={'display': 'inline-block'}),  # Ensure inline display
    
    # Sporting event selection dropdown
    html.Div([
        html.Label("Select Sporting Event"),
        dcc.Dropdown(
            id='sport-dropdown',
            options=[{'label': sport, 'value': sport} for sport in sporting_events],
            value=sporting_events[0],
            style={'margin-right': '40px', 'font-size': '16px', 'padding': '2px 15px'}  # Increased font size
        ),
    ], style={'display': 'inline-block'}),  # Ensure inline display
    
    # Gender analysis pie chart
    dcc.Graph(id='gender-analysis-pie')
])

# Define layout for preferences analysis page
preferences_layout = html.Div([
    html.H2("Viewer Preferences for Different Sports Events per country per continent", style={'textAlign': 'center'}),
    
    # Continent selection dropdown
    html.Div([
        html.Label("Select Continent", style={'marginRight': '10px'}),
        dcc.Dropdown(
            id='continent-dropdown',
            options=[{'label': continent, 'value': continent} for continent in continents],
            value=continents[0],  
            style={'margin-right': '50px', 'font-size': '16px', 'padding': '2px 30px'}
        ),
    ], style={'display': 'inline-block'}),

    # Country selection dropdown
    html.Div([
        html.Label("Select Country", style={'marginRight': '10px'}),
        dcc.Dropdown(
            id='country-dropdown',
            options=[],
            value='' ,
            style={'margin-right': '90px', 'font-size': '16px', 'padding': '2px 30px'}
        ),
    ], style={'display': 'inline-block'}),

    # Preferences analysis plot
    dcc.Graph(id='preferences-plot')
])

# Define layout for concurrent events page
layout_concurrent = html.Div([
    html.H2("Distribution of Concurrent Sporting Events by Viewer Engagement", style={'textAlign': 'center'}),

    # Dropdown for selecting month
    html.Div([
        html.Label("Select Month", style={'marginRight': '10px'}),
        dcc.Dropdown(
            id='month-dropdown-concurrent',
            options=[{'label': month, 'value': month} for month in months],
            value=months[0],
            clearable=False
        ),
    ]),

    # Heatmap plot for concurrent events
    dcc.Graph(id='concurrent-events-plot')
])

app.layout = html.Div([
        html.H1("FunOlympic Games Analysis Dashboard", style={'textAlign': 'center', 'marginBottom': '30px', 'fontFamily': 'Arial, sans-serif', 'color': '#333333'}),

    # Buttons for each analysis
    html.Div([
        html.Button('Viewship by Location', id='btn-geo', n_clicks=0, className='custom-button'),
        html.Button('Engagement Trends', id='btn-engagement', n_clicks=0, className='custom-button'),
        html.Button('Gender Analysis', id='btn-gender', n_clicks=0, className='custom-button'),
        html.Button('Preferences Analysis', id='btn-preferences', n_clicks=0, className='custom-button'),
        html.Button('Viewer Engagement', id='btn-navigation', n_clicks=0, className='custom-button'),
        html.Button('Concurrent Events', id='btn-concurrent', n_clicks=0, className='custom-button')
    ], className='btn-container', style={'textAlign': 'center', 'marginBottom': '30px'}),

    # Placeholder for selected analysis
    html.Div(id='analysis-output'),

     # Image
    html.Div([
        html.Img(src='/static/image/sport.jpg', style={'width': '35%', 'display': 'block', 'margin': 'auto'})
    ], style={'marginBottom': '30px'}),
    
])

# Define callback to update analysis output
@app.callback(
    Output('analysis-output', 'children'),
    [Input('btn-geo', 'n_clicks'),
     Input('btn-engagement', 'n_clicks'),
     Input('btn-gender', 'n_clicks'),
     Input('btn-preferences', 'n_clicks'),
     Input('btn-navigation', 'n_clicks'),
     Input('btn-concurrent', 'n_clicks')]
)
def update_analysis(btn_geo, btn_engagement, btn_gender, btn_preferences, btn_navigation, btn_concurrent):
    # Determine which button was clicked
    clicked_button = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    
    if clicked_button == 'btn-geo':
        # Return analysis based on clicked button
        layout_geo = html.Div([
            html.H2("Distribution of Viewship of Each Sporting Event by Geographic Location", style={'textAlign': 'center'}),
            
            # Dropdown for selecting sport viewed
            dcc.Dropdown(
                id='sport-viewed-dropdown',
                options=[{'label': sport, 'value': sport} for sport in df['Sport Viewed'].unique()],
                value=df['Sport Viewed'].unique()[0],
                clearable=False
            ),
            
            # Geographic plot for viewship distribution
            dcc.Graph(id='geographic-plot')
        ])
        return layout_geo
    elif clicked_button == 'btn-engagement':
        # Code to generate viewer engagement trends plot over time
        engagement_data = df.groupby(['Date']).size().reset_index(name='Viewership')
        fig = px.line(engagement_data, x='Date', y='Viewership')
        return html.Div([
            html.H2("Viewer Engagement Trends Over Time", style={'textAlign': 'center'}),
            # Dropdown for selecting month
            html.Div([
                html.Label("Select Month"),
                dcc.Dropdown(
                    id='month-dropdown',
                    options=[{'label': month, 'value': month} for month in df['Month'].unique()],
                    value=df['Month'].unique()[0], 
                    style={'margin-right': '30px', 'font-size': '16px', 'padding': '2px 30px'} # Added margin-right and increased font size
                ),
            ], style={'display': 'inline-block'}),  # Ensure inline display
            
            # Dropdown for selecting sporting event
            html.Div([
                html.Label("Select Sporting Event"),
                dcc.Dropdown(
                    id='sport-dropdown-engagement',
                    options=[{'label': sport, 'value': sport} for sport in df['Sport Viewed'].unique()],
                    value=df['Sport Viewed'].unique()[0], 
                    clearable=True,
                    placeholder="Select a Sporting Event",
                    style={'margin-right': '30px', 'font-size': '16px', 'padding': '2px 30px'} # Increased font size
                ),
            ], style={'display': 'inline-block'}),  # Ensure inline display

            dcc.Graph(id='engagement-plot', figure=fig)
        ])
    elif clicked_button == 'btn-gender':
        # Return gender analysis layout
        return gender_layout
    elif clicked_button == 'btn-preferences':
        # Return preferences analysis layout
        return preferences_layout
    elif clicked_button == 'btn-navigation':
        # Navigation patterns analysis
        navigation_layout = html.Div([
            html.H2("Viewer Engagement Patterns", style={'textAlign': 'center'}),
            dcc.Dropdown(
                id='navigation-dropdown',
                options=[
                    {'label': 'Request', 'value': 'Request'},
                    {'label': 'Rating', 'value': 'Rating'},
                    {'label': 'Feedback', 'value': 'Feedback'}
                ],
                value='Request', 
                clearable=False
            ),
            dcc.Graph(id='navigation-plot')
        ])
        return navigation_layout
    elif clicked_button == 'btn-concurrent':
        # Return concurrent events layout
        return layout_concurrent
    else:
        return html.Div("Select a requirement to display.", style={'textAlign': 'center','color': 'black', 'fontSize': '20px'})

# Callback to update geographic plot based on selected sport viewed
@app.callback(
    Output('geographic-plot', 'figure'),
    [Input('sport-viewed-dropdown', 'value')]
)
def update_geographic_plot(sport_viewed):
    # Filter dataframe based on selected sport viewed
    filtered_df = df[df['Sport Viewed'] == sport_viewed]
    
    # Group by country and count viewship
    viewship_by_country = filtered_df.groupby('Country').size().reset_index(name='Viewship')
    
    # Plot geographic distribution with color intensity based on viewership
    fig = px.scatter_geo(viewship_by_country, 
                         locations='Country', 
                         locationmode='country names',
                         size='Viewship',
                         projection='natural earth',
                         hover_name='Country',
                         title=f'Distribution of Viewship of {sport_viewed} by Geographic Location',
                         color='Viewship',  
                         color_continuous_scale='Viridis'  
                         )
    fig.update_layout(geo=dict(showcoastlines=True))
    fig.update_layout(height=550)  # Adjusting height of the graph
    return fig

# Callback to update engagement plot based on selected month and sporting event
@app.callback(
    Output('engagement-plot', 'figure'),
    [Input('month-dropdown', 'value'),
     Input('sport-dropdown-engagement', 'value')]
)
def update_engagement_plot(selected_month, selected_sport):
    # Filter dataframe based on selected month and sporting event
    filtered_df = df[(df['Month'] == selected_month) & (df['Sport Viewed'] == selected_sport)]
    
    # Group by date and count viewership
    engagement_data = filtered_df.groupby('Date').size().reset_index(name='Viewership')
    
    # Plot engagement trends
    fig = px.line(engagement_data, x='Date', y='Viewership', title=f'Viewer Engagement Trends for {selected_month} ({selected_sport})')
    return fig

# Callback to update gender analysis pie chart based on dropdown selection
@app.callback(
    Output('gender-analysis-pie', 'figure'),
    [Input('continent-dropdown', 'value'),
     Input('gender-dropdown', 'value'),
     Input('sport-dropdown', 'value')]
)
def update_gender_analysis_pie(continent, gender, sport):
    # Filter dataframe based on selected continent, gender, and sport
    filtered_df = df[(df['Continent'] == continent) & (df['Gender'] == gender) & (df['Sport Viewed'] == sport)]
    
    # Group by country and count occurrences
    country_counts = filtered_df['Country'].value_counts()
    
    # Create pie chart
    fig = px.pie(names=country_counts.index, values=country_counts.values)
    return fig

# Callback to update country dropdown based on continent selection
@app.callback(
    Output('country-dropdown', 'options'),
    [Input('continent-dropdown', 'value')]
)
def update_country_dropdown(continent):
    countries = df[df['Continent'] == continent]['Country'].unique()
    options = [{'label': country, 'value': country} for country in countries]
    return options

# Callback to update preferences analysis plot based on country selection
@app.callback(
    Output('preferences-plot', 'figure'),
    [Input('country-dropdown', 'value')]
)
def update_preferences_plot(country):
    filtered_df = df[df['Country'] == country]
    preferences_data = filtered_df['Sport Viewed'].value_counts().reset_index(name='Viewership')
    fig = px.bar(preferences_data, x='Sport Viewed', y='Viewership')
    fig.update_layout(xaxis_title='Sport Viewed', yaxis_title='Number of Viewership')
    return fig

# Callback to update navigation analysis plot based on dropdown selection
@app.callback(
    Output('navigation-plot', 'figure'),
    [Input('navigation-dropdown', 'value')]
)
def update_navigation_plot(selection):
    navigation_data = df.groupby(selection).size().reset_index(name='Viewership')
    fig = px.bar(navigation_data, x=selection, y='Viewership')
    fig.update_layout(xaxis_title=selection, yaxis_title='Number of Viewership')
    return fig

# Callback to update concurrent events plot based on selected month
@app.callback(
    Output('concurrent-events-plot', 'figure'),
    [Input('month-dropdown-concurrent', 'value')]
)
def update_concurrent_events_plot(selected_month):
    # Filter dataframe based on selected month
    filtered_df = df[df['Month'] == selected_month]

    # Group by sport viewed and week and count engagements
    engagement_summary = filtered_df.groupby(['Sport Viewed', 'Date']).size().reset_index(name='Engagement')

    # Create heatmap plot
    heatmap_fig = px.imshow(engagement_summary.pivot(index='Sport Viewed', columns='Date', values='Engagement'),
                            labels=dict(x="Date", y="Sport Viewed"),
                            title=f'Distribution of Concurrent Sporting Events for {selected_month} by Viewer Engagement')

    # Update layout to customize appearance
    heatmap_fig.update_layout(
        xaxis=dict(tickangle=45, title="Date"),
        yaxis=dict(title="Sport Viewed"),
        coloraxis=dict(colorscale="Blues")
    )

    return heatmap_fig

if __name__ == '__main__':
    app.run_server(debug=True)
