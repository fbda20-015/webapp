import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv('processed.csv')

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

# Title and description
st.title("FunOlympic Games Analysis Dashboard")
st.markdown("This dashboard allows you to analyze various aspects of the FunOlympic Games.")

# Sidebar
analysis_option = st.sidebar.radio("Select Analysis", ["Home", "Viewship by Location", "Engagement Trends", "Gender Analysis", "Preferences Analysis", "Viewer Engagement", "Concurrent Events"])

# Handle different analysis options
if analysis_option == "Home":
    st.header("Welcome to FunOlympic Games Analysis Dashboard")
    st.markdown("""
    This dashboard provides insights into the FunOlympic Games, including viewer engagement trends, preferences, and geographical distribution of viewership. 
    Use the sidebar to navigate through different analysis options.
    """)

elif analysis_option == "Viewship by Location":
    st.header("Distribution of Viewship of Each Sporting Event by Geographic Location")
    sport_viewed = st.selectbox("Select Sport Viewed", sporting_events)
    
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
    st.plotly_chart(fig)

elif analysis_option == "Engagement Trends":
    st.header("Viewer Engagement Trends Over Time")
    selected_month = st.selectbox("Select Month", months)
    selected_sport = st.selectbox("Select Sporting Event", sporting_events, index=0)
    
    # Filter dataframe based on selected month and sporting event
    filtered_df = df[(df['Month'] == selected_month) & (df['Sport Viewed'] == selected_sport)]
    
    # Group by date and count viewership
    engagement_data = filtered_df.groupby('Date').size().reset_index(name='Viewership')
    
    # Plot engagement trends
    fig = px.line(engagement_data, x='Date', y='Viewership', title=f'Viewer Engagement Trends for {selected_month} ({selected_sport})')
    st.plotly_chart(fig)

elif analysis_option == "Gender Analysis":
    st.header("Gender-specific Preferences and Behaviours")
    continent = st.selectbox("Select Continent", continents)
    gender = st.selectbox("Select Gender", genders)
    sport = st.selectbox("Select Sporting Event", sporting_events)
    
    # Filter dataframe based on selected continent, gender, and sport
    filtered_df = df[(df['Continent'] == continent) & (df['Gender'] == gender) & (df['Sport Viewed'] == sport)]
    
    # Group by country and count occurrences
    country_counts = filtered_df['Country'].value_counts()
    
    # Create pie chart
    fig = px.pie(names=country_counts.index, values=country_counts.values)
    st.plotly_chart(fig)

elif analysis_option == "Preferences Analysis":
    st.header("Viewer Preferences for Different Sports Events per country per continent")
    continent = st.selectbox("Select Continent", continents)
    country = st.selectbox("Select Country", df[df['Continent'] == continent]['Country'].unique())
    
    # Filter dataframe based on selected country
    filtered_df = df[df['Country'] == country]
    
    # Count viewership for each sport viewed
    preferences_data = filtered_df['Sport Viewed'].value_counts().reset_index(name='Viewership')
    fig = px.bar(preferences_data, x='Sport Viewed', y='Viewership')
    fig.update_layout(xaxis_title='Sport Viewed', yaxis_title='Number of Viewership')
    st.plotly_chart(fig)

elif analysis_option == "Viewer Engagement":
    st.header("Viewer Engagement Patterns")
    navigation_option = st.selectbox("Select Engagement Type", ['Request', 'Rating', 'Feedback'])
    
    # Group by selected engagement type and count occurrences
    navigation_data = df.groupby(navigation_option).size().reset_index(name='Viewership')
    fig = px.bar(navigation_data, x=navigation_option, y='Viewership')
    fig.update_layout(xaxis_title=navigation_option, yaxis_title='Number of Viewership')
    st.plotly_chart(fig)

elif analysis_option == "Concurrent Events":
    st.header("Distribution of Concurrent Sporting Events by Viewer Engagement")
    selected_month = st.selectbox("Select Month", months)
    
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
    st.plotly_chart(heatmap_fig)
