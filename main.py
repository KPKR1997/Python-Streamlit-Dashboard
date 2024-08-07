import streamlit as st
import plotly.express as px
import pandas as pd

#import mysql connection file
#from mysql_connection import *

#config page heads
st.set_page_config("Startup funding in India", page_icon="", layout="wide")
st.subheader("India Startup funding distribution")

#Frame data from database

result = pd.read_csv("STARTUP_DATA.csv")
df = pd.DataFrame(result, columns=[ "Startup","Industry", "City", "Amount"])

#Clean data


columns_to_transform = ['Startup', 'Industry']
df[columns_to_transform] = df[columns_to_transform].apply(lambda x: x.str.replace(' ', '').str.lower() if x.dtype == "object" else x)
df = df[df.apply(lambda x: (x != '').all(), axis=1)]  # Removes rows with empty strings
df = df.drop_duplicates(subset=["Startup"])
df['City'] = df['City'].str.replace('Bangalore', 'Bengaluru')
df['City'] = df['City'].str.replace('Gurgaon', 'Gurugram')




df.to_csv("new4.csv", index=False)


#DashboardLayout

#Sidebar

#Menu

from streamlit_option_menu import option_menu
with st.sidebar:
    selected = option_menu(
        menu_title = "Menu",
        options = ["Home", "Data"],
        icons = ["house", "book"],
        menu_icon =  "cast",
        default_index = 0,
        orientation = 'vertical',
    )


#Startup name filter

st.sidebar.header("Choose levels to explore")
startup = st.sidebar.multiselect(
    label = "Filter Company",
    options = df["Startup"].unique(),
    default = ["wealthbucket"]
)

#Startup type filter

industry = st.sidebar.multiselect(
    label = "Filter by Industry type",
    options = df["Industry"].unique(),
    default = ["fintech"]
)

#Startup City filter


city = st.sidebar.multiselect(
    label = "Filter by City",
    options = df["City"].unique(),
    default = ["New Delhi"]
)

#---------------------------------------------

#Process query


df_selection = df.query(
    "Startup == @startup & Industry == @industry & City == @city"
)

def metrics():
    from streamlit_extras.metric_cards import style_metric_cards
    col1, col2, col3 = st.columns(3)
    with col1:
        col1.metric("Total Companies", value=df_selection["Startup"].count(), delta="Number of Companies")
    with col2:
        col2.metric("Total Funded Amount (USD)", value=f"${df_selection['Amount'].sum():,.0f}", delta="Total Amount")

    style_metric_cards( background_color = "#071021", border_color="#F1F3F4")




#chart visualization
div1, div2 = st.columns(2)
def pie():
    with div1:
        theme_plotly = None
        fig = px.pie(df_selection, values="Amount", names= "Startup", title = "Industry")
        fig.update_layout(legend_title = "Startup", legend_y = 0.9)
        fig.update_traces(textinfo = "percent+label", textposition = "inside")
        st.plotly_chart(fig, use_container_width = True, theme =  theme_plotly)


def bar():
    with div2:
        theme_plotly = None
        fig = px.bar(df_selection, y = "Amount", x = "Startup", text_auto = "0.2s", title = "Bar chart")
        fig.update_traces(textfont_size = 18, textangle=0, textposition = "outside", cliponaxis=False)
        st.plotly_chart ( fig, use_container_width=True, theme = theme_plotly)


#Datatable for exploring

def table():
    with st.expander("choose companies in table format"):
        st.dataframe(df[["Startup", "Industry", "City"]], use_container_width = True, hide_index=True)


#st.dataframe(df)

if selected == "Home":
    pie()
    bar()
    metrics()
if selected == "Data":
    table()

