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

# Event types breakdown
st.header('Event Types')
event_types = filtered_df['event_type'].value_counts()
fig_event_types = px.pie(event_types,
                         values=event_types.values,
                         names=event_types.index)
st.plotly_chart(fig_event_types)

# Heatmap of performance locations
st.header('Performance Locations Heatmap')
fig_heatmap = px.density_mapbox(filtered_df,
                                lat='latitude',
                                lon='longitude',
                                zoom=1)
fig_heatmap.update_layout(mapbox_style="open-street-map")
st.plotly_chart(fig_heatmap)
