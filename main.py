import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page config
st.set_page_config(layout="wide", page_title="Headliners", page_icon="🎧")

# Custom CSS
st.markdown("""
<style>
    .reportview-container {
        background: #0e1117;
    }
    .main {
        background: #0e1117;
    }
    h1, h2, h3 {
        color: #ff4b4b;
    }
    .stSelectbox label, .stDateInput label {
        color: #fafafa;
    }
    .plot-container>div {
        border-radius: 5px;
        background: #262730;
    }
    .sidebar .sidebar-content {
        background-color: #262730;
    }
    .sidebar .sidebar-content * {
        color: #fafafa;
    }
    .sidebar .stDateInput > label {
        color: #ff4b4b !important;
        font-size: 1.2em !important;
        font-weight: bold !important;
    }
    .sidebar .stDateInput > div[data-baseweb="input"] {
        background-color: #3b3b3b !important;
    }
    .sidebar .stDateInput input {
        color: #fafafa !important;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
  df = pd.read_csv('data/dj_events_200.csv')
  df['date'] = pd.to_datetime(df['date'])
  return df

df = load_data()

# Main content
st.title('Headliners')

# First row: Date selector and Artist filter
col1, col2 = st.columns(2)

with col1:
    start_date, end_date = st.slider(
        'Select date range',
        min_value=df['date'].min().date(),
        max_value=df['date'].max().date(),
        value=(df['date'].min().date(), df['date'].max().date()),
        format="YYYY-MM-DD"
    )

with col2:
    artists = ['None'] + sorted(df['dj_name'].unique())
    selected_artist = st.selectbox('Select an artist', artists)

# Convert start_date and end_date to datetime
start_datetime = pd.to_datetime(start_date)
end_datetime = pd.to_datetime(end_date)

# Filter data based on date range and selected artist
filtered_df = df[(df['date'] >= start_datetime) & (df['date'] <= end_datetime)]
if selected_artist != 'None':
    artist_df = filtered_df[filtered_df['dj_name'] == selected_artist]
    
    # Define artist_tour for animation
    artist_tour = artist_df[['latitude', 'longitude', 'city', 'country', 'date']].copy()
    artist_tour['event_count'] = artist_tour.groupby(['city', 'country'])['date'].transform('count')
    artist_tour = artist_tour.sort_values('date')  # Ensure it's sorted by date
else:
    artist_df = filtered_df

# Top touring DJs
st.header('Top Touring DJs')
top_djs = filtered_df['dj_name'].value_counts().head(10)
fig_top_djs = px.bar(top_djs, x=top_djs.index, y=top_djs.values,
                     labels={'x': 'DJ Name', 'y': 'Number of Events'},
                     text=top_djs.values,
                     color=top_djs.values,
                     color_continuous_scale='Viridis')
fig_top_djs.update_traces(textposition='outside')
fig_top_djs.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font_color='#fafafa',
    xaxis_title=None,
    yaxis_title=None,
    xaxis={'showgrid': False},
    yaxis={'showgrid': False},
    showlegend=False,
    hovermode=False,
    coloraxis_showscale=False
)
st.plotly_chart(fig_top_djs, use_container_width=True)

if selected_artist != 'None':
    # Artist deep dive
    st.header(f'Deep Dive: {selected_artist}')

    # Create two columns for charts
    col1, col2 = st.columns(2)

    with col1:
        # Events by month
        st.subheader('Events by Month')
        artist_events_by_month = artist_df.groupby(artist_df['date'].dt.to_period('M')).size().reset_index(name='count')
        artist_events_by_month['date'] = artist_events_by_month['date'].dt.to_timestamp()
        artist_events_by_month['month_year'] = artist_events_by_month['date'].dt.strftime('%b %Y')
        
        fig_events_by_month = px.bar(artist_events_by_month, x='month_year', y='count',
                                     labels={'month_year': 'Month', 'count': 'Number of Events'},
                                     text='count')
        
        fig_events_by_month.update_traces(textposition='outside')
        fig_events_by_month.update_xaxes(tickangle=45, tickmode='linear')
        fig_events_by_month.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#fafafa',
            xaxis_title='Month',
            yaxis_title='Number of Events',
            bargap=0.2
        )
        st.plotly_chart(fig_events_by_month, use_container_width=True)

    with col2:
        # Event types for the selected artist
        st.subheader('Event Types')
        artist_event_types = artist_df['event_type'].value_counts()
        fig_artist_event_types = go.Figure(data=[go.Pie(labels=artist_event_types.index, 
                                                        values=artist_event_types.values,
                                                        hole=.3)])
        fig_artist_event_types.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#fafafa'
        )
        st.plotly_chart(fig_artist_event_types, use_container_width=True)

    # Performance Locations with Animation Option
    st.subheader('Performance Locations')

    # Group by location and count events
    location_counts = artist_df.groupby(['latitude', 'longitude', 'city', 'country']).size().reset_index(name='count')

    # Create scatter plot for venues
    fig_performance_locations = px.scatter_mapbox(location_counts,
                                                   lat='latitude',
                                                   lon='longitude',
                                                   size='count',
                                                   hover_name='city',
                                                   hover_data={'country': True, 'count': True, 'latitude': False, 'longitude': False},
                                                   zoom=1,
                                                   mapbox_style="carto-darkmatter",
                                                   size_max=25,
                                                   opacity=0.7,
                                                   color_discrete_sequence=['#FF4B4B'])

    # Set up the layout for the static view
    fig_performance_locations.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#fafafa',
        height=600
    )

    # Display the static chart
    chart_placeholder = st.empty()  # Create a placeholder for the chart
    chart_placeholder.plotly_chart(fig_performance_locations, use_container_width=True)

    # Button to trigger animation
    if st.button('Show Animation'):
        # Create frames for animation
        frames = []
        for k in range(1, len(artist_tour) + 1):
            current_tour = artist_tour.iloc[:k]  # Get the first k rows for the current frame
            event_counts = current_tour['city'].value_counts()

            frame = go.Frame(
                data=[go.Scattermapbox(
                    lat=current_tour['latitude'],
                    lon=current_tour['longitude'],
                    mode='markers+lines',
                    marker=dict(
                        size=current_tour['event_count'] * 3,  # Scale size for visibility
                        color='red',
                        opacity=0.7,  # Set opacity for better visibility
                    ),
                    text=current_tour['city'] + ', ' + current_tour['country'] + '<br>' + current_tour['date'].dt.strftime('%Y-%m-%d'),
                    hoverinfo='text',
                    name='Tour Route',
                )],
                traces=[0],
                name=f'frame{k}'
            )
            frames.append(frame)

        fig_performance_locations.frames = frames

        # Automatically start the animation
        fig_performance_locations.update_layout(
            updatemenus=[dict(
                type='buttons',
                showactive=False,
                buttons=[dict(
                    label='Play',
                    method='animate',
                    args=[None, dict(frame=dict(duration=500, redraw=True), mode='immediate')]
                )]
            )]
        )

        # Add slider for animation
        fig_performance_locations.update_layout(
            sliders=[dict(
                steps=[
                    dict(
                        method='animate',
                        args=[[f'frame{k}'], dict(mode='immediate', frame=dict(duration=500, redraw=True), transition=dict(duration=200))],
                        label=f'{k+1}'
                    ) for k in range(len(artist_tour))
                ],
                transition=dict(duration=200),
                x=0,
                y=0,
                currentvalue=dict(font=dict(size=12), prefix='Event: ', visible=True, xanchor='right'),
                len=1.0
            )]
        )

        # Update the existing chart in the placeholder with the animation
        chart_placeholder.plotly_chart(fig_performance_locations, use_container_width=True)

        # Simulate the play button click by updating the chart again
        chart_placeholder.plotly_chart(fig_performance_locations, use_container_width=True, config={'displayModeBar': False})

    # Display some key stats
    total_events = len(artist_df)
    total_cities = artist_df['city'].nunique()
    total_countries = artist_df['country'].nunique()

    st.header("Key Stats")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Events", total_events)
    col2.metric("Cities Visited", total_cities)
    col3.metric("Countries Toured", total_countries)

    # Event list
    st.header("Event List")
    today = pd.Timestamp.now().date()
    
    def event_row_style(row):
        if row['date'].date() < today:
            return ['color: gray'] * len(row)
        elif row['date'].date() > today:
            return ['font-weight: bold'] * len(row)
        else:
            return [''] * len(row)
    
    event_list = artist_df[['date', 'city', 'country', 'event_type']].sort_values('date',ascending=False)
    styled_event_list = event_list.style.apply(event_row_style, axis=1)
    st.dataframe(styled_event_list, use_container_width=True)

else:
    st.info("Select an artist to see detailed information.")
