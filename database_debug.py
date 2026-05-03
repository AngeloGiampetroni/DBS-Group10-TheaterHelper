import streamlit as st
from database.theater_helper import TheaterDBHelper

# Connect to the database
conn = st.connection("mysql", type="sql")
db = TheaterDBHelper(conn)

st.title("Theater Helper Debug")

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
