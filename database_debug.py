import streamlit as st
from database.theater_helper import TheaterDBHelper

# Connect to the database
conn = st.connection("mysql", type="sql")
db = TheaterDBHelper(conn)

st.title("Theater Helper Debug")

# SELECT query
st.subheader("Execute SQL queries - !!!Use SELECT QUERIES ONLY!!!")
query = st.text_area("Enter your SQL query here:")
if st.button("Run Query"):
        try:
            results = db.get_query(query)
            st.dataframe(results)
        except Exception as e:
            st.error(f"Error occurred while running query: {e}")

#Adding new customer
st.subheader("Add Customer")
with st.form("customer_form", clear_on_submit=True):
    f_name = st.text_input("First Name")
    l_name = st.text_input("Last Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    age = st.number_input("Age", min_value=1, max_value=120, step=1)
    
    if st.form_submit_button("Save Customer"):
        if f_name and l_name and email:
            db.add_customer(f_name, l_name, email, phone, age)
            st.success(f"Customer {f_name} {l_name} added!")
        else:
            st.warning("Please fill out the required fields.")

#Adding new movie
st.subheader("Add Movie")
with st.form("movie_form", clear_on_submit=True):
    title = st.text_input("Title")
    studio = st.text_input("Studio")
    genre = st.text_input("Genre")
    age_rating = st.text_input("Age Rating")    
    runtime = st.text_input("Runtime (HH:MM:SS)")
    
    if st.form_submit_button("Save Movie"):
        if title and studio:
            db.add_movie(title, studio, genre, age_rating, runtime)
            st.success(f"Movie {title} added!")
        else:
            st.warning("Please fill out the required fields.")

# Adding Ticket
st.subheader("Add Ticket")
with st.form("ticket_form", clear_on_submit=True):
    customer_id = st.number_input("Customer ID", min_value=1)
    movie_id = st.number_input("Movie ID", min_value=1)
    show_id = st.number_input("Show ID", min_value=1)
    price = st.number_input("Price", min_value=0.0)
    if st.form_submit_button("Add Ticket"):
        if customer_id and movie_id and show_id:
            db.add_ticket(customer_id, movie_id, show_id, price)
            st.success(f"Ticket added for Customer ID {customer_id}!")
        else:
            st.warning("Please fill out the required fields.")

# Updating Customer
st.subheader("Update Customer")
with st.form("update_customer_form", clear_on_submit=True):
    customer_id = st.number_input("Customer ID", min_value=1, value=None)
    first_name = st.text_input("First Name", value=None)
    last_name = st.text_input("Last Name", value=None)
    email = st.text_input("Email", value=None)
    phone = st.text_input("Phone Number", value=None)
    age = st.number_input("Age", min_value=1, max_value=120, step=1, value=None)

    if st.form_submit_button("Update Customer"):
        if customer_id:
            db.update_customer(customer_id, first_name, last_name, email, phone, age)
            st.success(f"Customer ID {customer_id} updated!")
        else:
            st.warning("Please enter a valid Customer ID.")

# Updating Movie
st.subheader("Update Movie")
with st.form("update_movie_form", clear_on_submit=True):
    movie_id = st.number_input("Movie ID", min_value=1, value=None)
    title = st.text_input("Title", value=None)
    studio = st.text_input("Studio", value=None)
    genre = st.text_input("Genre", value=None)
    age_rating = st.text_input("Age Rating", value=None)
    runtime = st.text_input("Runtime (HH:MM:SS)", value=None)

    if st.form_submit_button("Update Movie"):
        if movie_id:
            db.update_movie(movie_id, title, studio, genre, age_rating, runtime)
            st.success(f"Movie ID {movie_id} updated!")
        else:
            st.warning("Please enter a valid Movie ID.")

# Updating Showing
st.subheader("Update Showing")
with st.form("update_showing_form", clear_on_submit=True):  
    show_id = st.number_input("Show ID", min_value=1, value=None)   
    movie_id = st.number_input("Movie ID", min_value=1, value=None)
    room_number = st.text_input("Room Number", value=None)
    date = st.date_input("Date", value=None)
    time = st.time_input("Time", value=None)

    if st.form_submit_button("Update Showing"):
        if show_id:
            db.update_showing(show_id, movie_id, room_number, date, time)
            st.success(f"Showing ID {show_id} updated!")
        else:
            st.warning("Please enter a valid Show ID.")

# Updating Ticket
st.subheader("Update Ticket")
with st.form("update_ticket_form", clear_on_submit=True):
    ticket_id = st.number_input("Ticket ID", min_value=1, value=None)
    customer_id = st.number_input("Customer ID", min_value=1, value=None)
    movie_id = st.number_input("Movie ID", min_value=1, value=None)
    show_id = st.number_input("Show ID", min_value=1, value=None)
    price = st.number_input("Price", min_value=0.0, value=None)

    if st.form_submit_button("Update Ticket"):
        if ticket_id:
            db.update_ticket(ticket_id, customer_id, movie_id, show_id, price)
            st.success(f"Ticket ID {ticket_id} updated!")
        else:
            st.warning("Please enter a valid Ticket ID.")
