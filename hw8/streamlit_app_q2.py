"""
I should be able to click on radio buttons in the sidebar and be taken to various pages.
Add an interactive plot using plotly, and place that on a separate page.
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# App title
apptitle = 'Earthquake Data Analysis'

# Setting page configuration
st.set_page_config(page_title=apptitle, page_icon=":bear:")

# Sidebar setup
st.sidebar.markdown("## Sidebar")

# File uploader widget
my_file = st.sidebar.file_uploader("Upload your file here")
if my_file is not None:
    df = pd.read_csv(my_file)
else:
    df = None

# Options for data analysis
st.sidebar.markdown("### Data Analysis Options")
option = st.sidebar.radio("Select the option: ", ["Home", "Data Header", "Data Summary", "Scatter Plot", "Interactive Plot"])

# Main app title
st.title(apptitle)

# Handling navigation and display based on user selection
if option == "Home":
    st.markdown("### This is an app that explores earthquake data.")
    st.markdown("""
        * Upload your data using the sidebar.
        * Navigate the sidebar to select the information you wish to explore.
        * The results will be displayed.
    """)

elif option == "Data Header" and df is not None:
    st.markdown("### Preview of the Data")
    st.write(df.head())

elif option == "Data Summary" and df is not None:
    st.markdown("### Summary Statistics of Data")
    st.write(df.describe())

elif option == "Scatter Plot" and df is not None:
    st.markdown("### Plot of Data")
    fig, ax = plt.subplots()
    ax.scatter(x=df["Depth"], y=df["Magnitude"])
    ax.set_xlabel("Depth")
    ax.set_ylabel("Magnitude")
    st.pyplot(fig)

elif option == "Interactive Plot" and df is not None:
    st.markdown("### Interactive Plot of Data")
    if 'Date' in df.columns and 'Time' in df.columns:
        df['DateTime'] = df['Date'] + ' ' + df['Time']
    fig = px.scatter(df, x="Depth", y="Magnitude", hover_name="DateTime")
    st.plotly_chart(fig)

else:
    if df is None:
        st.warning("Please upload a file to proceed.")
    else:
        st.write("Please select an option from the sidebar.")