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

@st.dialog("Book a Ticket")
def book_ticket_dialog(customer):
    st.write(f"Booking for: **{customer.first_name} {customer.last_name}**")
    
    # Fetch available showings
    showings = db.get_query("SELECT * FROM theater.showing;")

    
    if showings.empty:
        st.error("No showings available at this time.")
        return

    # Create a list of options for the dropdown
    # Formats the list so users see: "Movie Title | Room 4 | 19:00:00"
    options = {
        f"{row['movie']} | Room {row['room_number']} | {row['date']} at {row['time']}": {
            "showing_id": row["id"],
            "movie_id": row["movie"],
        }
        for _, row in showings.iterrows()
    }
    
    
    selected_label = st.selectbox("Choose a Showing", options)
    selected_data = options[selected_label]
    
    price = float("9.99")

    if st.button("Confirm Purchase", use_container_width=True):
        success = db.add_ticket(
            customer_id=customer.id,
            movie_id=selected_data['movie_id'],
            show_id=selected_data['showing_id'],
            price=price
        )
        
        if success:
            st.success("Ticket purchased!")
            print("Ticket purchased!")
            st.rerun() # Refresh to show the new ticket in the table

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
    tab_list_tickets, tab_current_movies = st.tabs(["My Tickets", "Current Movies"])
    with tab_list_tickets:
        col_1, col_2 = st.columns(2)
        with col_1:
            st.subheader("My Tickets")
            st.dataframe(
                db.get_all_tickets_by_customer(customer.id),
                use_container_width=True,
                hide_index=True,
            )
        with col_2:
            if st.button("Book A Ticket", use_container_width=True):
                book_ticket_dialog(customer)
    with tab_current_movies:
        st.subheader("Current Movies")
        st.subheader("Lobby poster wall")
        #mview = movies_df[movies_df["genre"].isin(genre_filter)].reset_index(drop=True)
        mview = db.get_movies_with_filters(genre=genre_filter if genre_filter else None)
        for start in range(0, len(mview), 4):
            chunk = mview.iloc[start : start + 4]
            cols = st.columns(4)
            for j, (_, row) in enumerate(chunk.iterrows()):
                with cols[j]:
                    st.markdown(
                        f"""
                        <div class="poster">
                            <div class="poster-title">{row['title']}</div>
                            <div class="poster-meta">{row['genre']} · {row['age_rating']}<br/>
                            {row['runtime']}<br/><span style="opacity:0.85">{row['studio']}</span></div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
        
    


# Main app logic
if st.session_state.customer_data is not None:
    display_dashboard()
else:
    login()