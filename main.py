import streamlit as st
import pandas as pd
import plotly.express as px


# Load data
@st.cache_data
def load_data():
  df = pd.read_csv('dj_events_200.csv')
  df['date'] = pd.to_datetime(df['date'])
  return df


df = load_data()

st.title('DJ Tour Analytics Dashboard')

# Date range selector
start_date, end_date = st.date_input('Select date range',
                                     [df['date'].min().date(), df['date'].max().date()])

# Convert start_date and end_date to datetime
start_datetime = pd.to_datetime(start_date)
end_datetime = pd.to_datetime(end_date)

# Filter data based on date range
filtered_df = df[(df['date'] >= start_datetime) & (df['date'] <= end_datetime)]

# Top touring DJs
st.header('Top Touring DJs')
top_djs = filtered_df['dj_name'].value_counts().head(10)
fig_top_djs = px.bar(top_djs, x=top_djs.index, y=top_djs.values)
st.plotly_chart(fig_top_djs)


# Artist deep dive
st.header('Artist Deep Dive')

# Get list of unique artists
artists = sorted(filtered_df['dj_name'].unique())

# Dropdown to select an artist
selected_artist = st.selectbox('Select an artist', artists)

# Filter data for the selected artist
artist_df = filtered_df[filtered_df['dj_name'] == selected_artist]

# Events by month
st.subheader(f'Events by Month for {selected_artist}')
artist_events_by_month = artist_df.groupby(artist_df['date'].dt.to_period('M')).size().reset_index(name='count')
artist_events_by_month['date'] = artist_events_by_month['date'].dt.to_timestamp()
fig_events_by_month = px.bar(artist_events_by_month, x='date', y='count')
st.plotly_chart(fig_events_by_month)

# Event types for the selected artist
st.subheader(f'Event Types for {selected_artist}')
artist_event_types = artist_df['event_type'].value_counts()
fig_artist_event_types = px.pie(artist_event_types,
                                values=artist_event_types.values,
                                names=artist_event_types.index)
st.plotly_chart(fig_artist_event_types)

# Heatmap of performance locations for the selected artist
st.subheader(f'Performance Locations Heatmap for {selected_artist}')
fig_artist_heatmap = px.density_mapbox(artist_df,
                                       lat='latitude',
                                       lon='longitude',
                                       zoom=1)
fig_artist_heatmap.update_layout(mapbox_style="open-street-map")
st.plotly_chart(fig_artist_heatmap)
