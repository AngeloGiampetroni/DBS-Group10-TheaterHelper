import os
import sys

import pandas as pd
import plotly.express as px
import streamlit as st
from database.database_helper import TheaterDBHelper
from theater_css import THEATER_CSS

st.set_page_config(
    page_title="Customer Dashboard",
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

# Initialize session state - customer data
if "customer_data" not in st.session_state:
    st.session_state.customer_data = None


st.title("Customer Dashboard")

def login():
    with st.container():
        st.markdown("### Login")
        customer_id = st.number_input(
            "Enter your Customer ID:",
            key="login_customer_id",
            step=1,
            min_value=1,
        )
        
        if st.button("Login", use_container_width=True, key="login_button"):
            # Customer exists
            customer = db.get_customer_by_id(customer_id)
            if customer:
                st.session_state.customer_data = customer
                st.rerun()
            else:
                st.error("Customer ID not found. Please try again.")


def logout():
    """Clear login session"""
    st.session_state.customer_data = None
    st.rerun()


def display_dashboard():
    
    with st.sidebar:
        if st.button("Logout", key="logout_button"):
            logout()
    
    customer = st.session_state.customer_data
    
    if customer:
        st.subheader(f"Welcome, {customer.first_name} {customer.last_name}!")
        st.markdown(f"Customer ID: {customer.id}")
        st.markdown(f"Email: {customer.email}")
        st.markdown(f"Phone: {customer.phone_number}")
        st.markdown(f"Age: {customer.age}")
        st.markdown(f"Member since {customer.date_entered}")
        #TODO add data the customer should look at
        display_content(customer=customer)

        
    else:
        st.error("Error loading customer information. Please log in again.")
        if st.button("Back to Login"):
            logout()

def display_content(customer):
    tab_list_tickets, tab_current_movies = st.tabs(["My Tickets", "Current Movies"])
    with tab_list_tickets:
        st.subheader("My Tickets")
        st.dataframe(
            db.get_all_tickets_by_customer(customer.id),
            use_container_width=True,
            hide_index=True,
        )

# Main app logic
if st.session_state.customer_data is not None:
    display_dashboard()
else:
    login()