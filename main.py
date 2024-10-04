import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page config
st.set_page_config(layout="wide", page_title="DJ Tour Analytics", page_icon="🎧")

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
  df = pd.read_csv('dj_events_200.csv')
  df['date'] = pd.to_datetime(df['date'])
  return df

df = load_data()

# Main content
st.title('DJ Tour Analytics Dashboard')

# First row: Date selector and Artist filter
col1, col2 = st.columns(2)

with col1:
    start_date, end_date = st.date_input(
        'Select date range',
        [df['date'].min().date(), df['date'].max().date()],
        label_visibility="visible"
    )

with col2:
    artists = sorted(df['dj_name'].unique())
    selected_artist = st.selectbox('Select an artist', artists)

# Convert start_date and end_date to datetime
start_datetime = pd.to_datetime(start_date)
end_datetime = pd.to_datetime(end_date)

# Filter data based on date range and selected artist
filtered_df = df[(df['date'] >= start_datetime) & (df['date'] <= end_datetime)]
artist_df = filtered_df[filtered_df['dj_name'] == selected_artist]

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
    title={
        'text': 'Top 10 Touring DJs',
        'font': {'size': 24, 'color': '#ff4b4b'}
    },
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font_color='#fafafa',
    xaxis_title=None,
    yaxis_title=None,
    xaxis={'showgrid': False},
    yaxis={'showgrid': False},
    showlegend=False,
    hovermode=False,
    coloraxis_showscale=False  # Hide color scale legend
)
st.plotly_chart(fig_top_djs, use_container_width=True)

# Artist deep dive
st.header('Artist Deep Dive')

# Create two columns for charts
col1, col2 = st.columns(2)

with col1:
    # Events by month
    st.subheader(f'Events by Month for {selected_artist}')
    artist_events_by_month = artist_df.groupby(artist_df['date'].dt.to_period('M')).size().reset_index(name='count')
    artist_events_by_month['date'] = artist_events_by_month['date'].dt.to_timestamp()
    fig_events_by_month = px.bar(artist_events_by_month, x='date', y='count',
                                 labels={'date': 'Month', 'count': 'Number of Events'},
                                 title=f'Events by Month for {selected_artist}')
    fig_events_by_month.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#fafafa'
    )
    st.plotly_chart(fig_events_by_month, use_container_width=True)

with col2:
    # Event types for the selected artist
    st.subheader(f'Event Types for {selected_artist}')
    artist_event_types = artist_df['event_type'].value_counts()
    fig_artist_event_types = go.Figure(data=[go.Pie(labels=artist_event_types.index, 
                                                    values=artist_event_types.values,
                                                    hole=.3)])
    fig_artist_event_types.update_layout(
        title=f'Event Types for {selected_artist}',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#fafafa'
    )
    st.plotly_chart(fig_artist_event_types, use_container_width=True)

# Heatmap of performance locations for the selected artist
st.subheader(f'Performance Locations Heatmap for {selected_artist}')
fig_artist_heatmap = px.density_mapbox(artist_df,
                                       lat='latitude',
                                       lon='longitude',
                                       zoom=1,
                                       mapbox_style="carto-darkmatter")
fig_artist_heatmap.update_layout(
    title=f'Performance Locations Heatmap for {selected_artist}',
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font_color='#fafafa'
)
st.plotly_chart(fig_artist_heatmap, use_container_width=True)

# Display some key stats
total_events = len(artist_df)
total_cities = artist_df['city'].nunique()
total_countries = artist_df['country'].nunique()

st.header("Key Stats")
col1, col2, col3 = st.columns(3)
col1.metric("Total Events", total_events)
col2.metric("Cities Visited", total_cities)
col3.metric("Countries Toured", total_countries)
