import os
import sys

import plotly.express as px
import streamlit as st
from database.database_helper import TheaterDBHelper
from theater_css import THEATER_CSS

st.set_page_config(
    page_title="Admin Dashboard",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Connect to the database
conn = st.connection("mysql", type="sql")
db = TheaterDBHelper(conn)

_PAGES_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PAGES_DIR not in sys.path:
    sys.path.insert(0, _PAGES_DIR)

st.markdown(f"<style>{THEATER_CSS}</style>", unsafe_allow_html=True)

st.markdown("# Admin Dashboard")
st.caption("Manage your theater's operations and view key metrics.")


with st.sidebar:
    st.markdown("### Concessions & filters")
    st.markdown("---")
    date_opts = ["All dates"] + sorted(db.get_showing_dates()["date"].tolist())
    pick_date = st.selectbox("Showtime date", date_opts)
    genre_filter = st.multiselect(
        "Genres on screen",
        options=sorted(db.get_all_genres()["genre"].tolist()),
        default=None,
    )
    st.markdown("---")
    st.markdown(
        "<small>Velvet seats • digital projection • hearing-assisted devices available</small>",
        unsafe_allow_html=True,
    )

filt_schedule = db.get_showing_dates()
if pick_date != "All dates":
    filt_schedule = filt_schedule[filt_schedule["date"] == pick_date]

tab_analytics, tab_schedule, tab_customers, tab_sql = st.tabs(
    ["Analytics", "Film Schedule Management", "Change Customer Data", "SQL Query Console"]
)

with tab_analytics:
    st.subheader("Analytics")
    tabsales, tabgenre = st.tabs(["Sales by Movie", "Revenue by Genre"])
    with tabsales:
        data = db.ticket_sales_by_movie() # title, tickets_sold, revenue
        st.plotly_chart(px.bar(data, x="title", y=["tickets_sold", "revenue"], barmode="group"), use_container_width=True)
        st.dataframe(data, use_container_width=True, hide_index=True)
    with tabgenre:
        data = db.ticket_sales_by_genre() # genre, tickets_sold, revenue
        st.plotly_chart(px.bar(data, x="genre", y=["tickets_sold", "revenue"], barmode="group"), use_container_width=True)
        st.dataframe(data, use_container_width=True, hide_index=True)
        

with tab_schedule:
    st.subheader("Film Schedule Management")
    st.markdown("Here you can add, edit, or remove film showings.")
    #TODO

with tab_customers:
    st.subheader("Change Customer Data")
    st.markdown("Manage customer information and preferences.")
    #TODO

with tab_sql:
    st.subheader("SQL Query Console")
    st.markdown("Run custom SQL queries against your database.")
    query = st.text_area("Enter your SQL query here:")
    if st.button("Run Query"):
        try:
            result = db.get_query(query)
            st.dataframe(result)
        except Exception as e:
            st.error(f"Error executing query: {e}")
