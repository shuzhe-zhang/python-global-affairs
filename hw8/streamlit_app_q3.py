import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt
from vega_datasets import data

# Function for heatmap visualization
def show_heatmap(df_reshaped):
    """
    Renders a population heatmap by state and year in the Streamlit app.

    Args:
    df_reshaped (DataFrame): The reshaped DataFrame with population data.
    """
    heatmap = alt.Chart(df_reshaped).mark_rect().encode(
        y=alt.Y('year:O', axis=alt.Axis(title="Year", titleFontSize=16, titlePadding=15, titleFontWeight=900, labelAngle=0)),
        x=alt.X('states:O', axis=alt.Axis(title="States", titleFontSize=16, titlePadding=15, titleFontWeight=900)),
        color=alt.Color('max(population):Q', scale=alt.Scale(scheme="blueorange")),
        stroke=alt.value('black'),
        strokeWidth=alt.value(0.25)
    ).properties(width=900).configure_axis(labelFontSize=12, titleFontSize=12)
    st.altair_chart(heatmap, use_container_width=True)

# Function for geographical map visualization
def show_geo_map(df_reshaped, selected_year):
    """
    Plots a U.S. geographical map of population for a selected year using Altair.

    Args:
    df_reshaped (DataFrame): The DataFrame with population data by state and year.
    selected_year (int): The year for which to filter and display population data.
    """
    df_selected_year = df_reshaped[df_reshaped["year"] == selected_year]

    states = alt.topo_feature(data.us_10m.url, 'states')
    geo_chart = alt.Chart(states).mark_geoshape().encode(
        color=alt.Color('population:Q', scale=alt.Scale(scheme='blues')),
        stroke=alt.value('#154360')
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(df_selected_year, 'id', ['population'])
    ).properties(
        width=500,
        height=300
    ).project(type='albersUsa')
    st.altair_chart(geo_chart, use_container_width=True)


# Load data
df = pd.read_csv("us-population-2010-2019-states-code.csv")
df_reshaped = pd.melt(df, id_vars=['states', 'states_code', 'id'],
                      var_name='year', value_name='population')
df_reshaped['year'] = df_reshaped['year'].astype(int)
df_reshaped['states'] = df_reshaped['states'].astype('string')
df_reshaped['population'] = df_reshaped['population'].str.replace(',', '').astype(int)

# Streamlit UI
# App title
apptitle = 'US Population Analysis'
# Setting page configuration
st.set_page_config(page_title=apptitle, page_icon=":bear:")

# Sidebar setup
st.sidebar.markdown("## Sidebar")
st.sidebar.markdown("### Data Analysis Options")
page = st.sidebar.radio("Select the option:", ["Home", "Heatmap", "Geographical Map"])

# Main app title
st.title(apptitle)

if page == "Home":
    st.markdown("### This is an app that explores US Census Data.")
    st.markdown("""
            * Navigate the sidebar to select the information you wish to explore.
            * The results will be displayed.
        """)

elif page == "Heatmap":
    st.markdown("### Population Heatmap")
    show_heatmap(df_reshaped)

elif page == "Geographical Map":
    st.markdown("### Population Geographical Map")
    selected_year = st.sidebar.slider("Select Year:", min_value=int(df_reshaped['year'].min()),
                                      max_value=int(df_reshaped['year'].max()), value=2019)
    show_geo_map(df_reshaped, selected_year)