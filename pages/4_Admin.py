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

tab_analytics, tab_schedule, tab_customers, tab_movies, tab_sql = st.tabs(
    ["Analytics", "Film Schedule Management", "Customer Management", "Movie Inventory", "SQL Query Console"]
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
    # --- Add Showing ---
    with st.expander("Add New Showing", expanded=False):
        with st.form("add_showing_form", clear_on_submit=True):
            movies_df = db.get_query("SELECT id, title FROM theater.movie ORDER BY title")
            movie_options = {
                f"{row['title']} (ID: {row['id']})": row['id']
                for _, row in movies_df.iterrows()
            }

            selected_movie = st.selectbox("Movie", movie_options.keys())
            room = st.text_input("Room Number", value="1")
            show_date = st.date_input("Date")
            show_time = st.time_input("Time")

            if st.form_submit_button("Add Showing"):
                success = db.add_showing(
                    movie_id=movie_options[selected_movie],
                    room_number=room,
                    date=show_date,
                    time=show_time.strftime("%H:%M:%S"),
                )
                if success:
                    st.success("Showing added.")
                    st.rerun()

    # --- View Showings ---
    with st.expander("Current Showings", expanded=True):
        showings_df = db.get_query("""
            SELECT s.id, m.title AS movie, s.room_number, s.date, s.time
            FROM theater.showing s
            JOIN theater.movie m ON s.movie = m.id
            ORDER BY s.date DESC, s.time DESC
        """)
        st.dataframe(showings_df, use_container_width=True, hide_index=True)

    # --- Remove Showing ---
    with st.expander("Remove Showing", expanded=False):
        with st.form("remove_showing_form", clear_on_submit=True):
            showing_ids = [row['id'] for _, row in showings_df.iterrows()]
            remove_id = st.selectbox("Showing ID to remove", showing_ids)
            st.warning("This will cancel all tickets for this showing.")

            if st.form_submit_button("Remove Showing"):
                tickets_removed = db.remove_all_tickets_for_showing(remove_id)
                if tickets_removed >= 0:
                    success = db.remove_showing(remove_id)
                    if success:
                        st.success(
                            f"Showing {remove_id} removed. "
                            f"{tickets_removed} ticket(s) canceled."
                        )
                else:
                    st.error("Failed to remove tickets. Showing was not removed.")
                st.rerun()

with tab_customers:
    st.subheader("Change Customer Data")
    st.markdown("Manage customer information and preferences.")
    # --- Add Customer ---
    with st.expander("Add New Customer", expanded=False):
        with st.form("add_customer_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                fname = st.text_input("First Name")
                email = st.text_input("Email")
            with col2:
                lname = st.text_input("Last Name")
                phone = st.text_input("Phone Number")
            age = st.number_input("Age", min_value=1, max_value=120, value=None)
            
            if st.form_submit_button("Add Customer"):
                if fname and lname and email:
                    success = db.add_customer(fname, lname, email, phone, age)
                    if success:
                        st.success(f"Customer {fname} {lname} added.")
                        st.rerun()
                else:
                    st.warning("First name, last name, and email are required.")

    # --- Update Customer ---
    with st.expander("Update Existing Customer", expanded=False):
        customers_df = db.get_query("SELECT id, first_name, last_name, email FROM theater.customer ORDER BY id")
        customer_options = {f"{row['first_name']} {row['last_name']} (ID: {row['id']})": row['id'] for _, row in customers_df.iterrows()}
        
        selected_cust = st.selectbox("Select Customer", customer_options.keys())
        cust_id = customer_options[selected_cust]
        
        with st.form("update_customer_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                new_fname = st.text_input("New First Name", value=None)
                new_email = st.text_input("New Email", value=None)
            with col2:
                new_lname = st.text_input("New Last Name", value=None)
                new_phone = st.text_input("New Phone Number", value=None)
            new_age = st.number_input("New Age", min_value=1, max_value=120, value=None)
            
            if st.form_submit_button("Update Customer"):
                success = db.update_customer(
                    customer_id=cust_id,
                    first_name=new_fname,
                    last_name=new_lname,
                    email=new_email,
                    phone=new_phone,
                    age=new_age
                )
                if success:
                    st.success("Customer updated.")
                    st.rerun()

    # --- Remove Customer ---
    with st.expander("Remove Customer", expanded=False):
        st.warning("This will also remove all tickets belonging to this customer.")
        
        with st.form("remove_customer_form", clear_on_submit=True):
            cust_del_id = st.number_input("Customer ID to remove", min_value=1, step=1)
            if st.form_submit_button("Remove Customer"):
                success = db.remove_customer(cust_del_id)
                if success:
                    st.success(f"Customer {cust_del_id} removed.")
                    st.rerun()

    # --- Manage Customer Tickets ---
    with st.expander("Manage Tickets for a Customer", expanded=False):
        with st.form("cust_tickets_form", clear_on_submit=True):
            search_id = st.number_input("Customer ID", min_value=1, step=1)
            if st.form_submit_button("View / Remove Tickets"):
                tickets = db.get_all_tickets_by_customer(search_id)
                if tickets.empty:
                    st.info("No tickets found for this customer.")

with tab_movies:
    st.subheader("Movie Inventory")
    # --- Add Movie ---
    with st.expander("Add New Movie", expanded=False):
        with st.form("add_movie_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                title = st.text_input("Title")
                genre = st.selectbox(
                    "Genre",
                    ["Action", "Comedy", "Drama", "Horror", "Romance",
                     "Sci-Fi", "Thriller", "Animation", "Fantasy", "Sports"],
                )
                age_rating = st.selectbox("Age Rating", ["G", "PG", "PG-13", "R", "NC-17"])
            with col2:
                studio = st.text_input("Studio")
                runtime = st.time_input("Runtime")

            if st.form_submit_button("Add Movie"):
                if title and studio:
                    runtime_str = runtime.strftime("%H:%M:%S") if runtime else None
                    success = db.add_movie(title, studio, genre, age_rating, runtime_str)
                    if success:
                        st.success(f"'{title}' added.")
                        st.rerun()
                else:
                    st.warning("Title and studio are required.")

    # --- View Movies ---
    with st.expander("Current Movies", expanded=True):
        movies_df = db.get_query("SELECT * FROM theater.movie ORDER BY id DESC")
        st.dataframe(movies_df, use_container_width=True, hide_index=True)

    # --- Remove Movie ---
    with st.expander("Remove Movie", expanded=False):
        with st.form("remove_movie_form", clear_on_submit=True):
            remove_movie_id = st.number_input("Movie ID to remove", min_value=1, step=1)
            st.warning(
                "This will remove all showings and cancel all tickets for this movie."
            )

            if st.form_submit_button("Remove Movie"):
                result = db.remove_all_showings_for_movie(remove_movie_id)
                if result:
                    success = db.remove_movie(remove_movie_id)
                    if success:
                        st.success(
                            f"Movie {remove_movie_id} removed. "
                            f"{result['showings_removed']} showing(s) and "
                            f"{result['tickets_removed']} ticket(s) deleted."
                        )
                else:
                    st.error("Failed to remove showings. Movie was not removed.")
                st.rerun()

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
