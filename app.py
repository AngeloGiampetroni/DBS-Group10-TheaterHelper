import streamlit as st

st.set_page_config(
    page_title="Home",
    page_icon="🎬",
    layout="wide",
)

st.title("Welcome")
st.markdown("""
This app is a small **Streamlit** frontend. Use the **sidebar** (left) to open other pages:

- **Theater Helper** — showtimes, posters, and ticket stats from your theater database data  
- **Chatbot** — simple chat demo  
- **About** — how the app is put together  
""")

st.markdown("---")
st.subheader("Where is the theater data?")
st.markdown("""
Your sample data lives in **`TheaterHelperDB.sql`** (in this same `src/pages/` folder).  
It is meant to be loaded into a MySQL database named `theater` (tables: `movie`, `customer`, `showing`, `ticket`).

The **Theater Helper** page does not need MySQL: it reads the same rows through **`theater_data.py`**, which mirrors that SQL file so the website can show movies, showtimes, and tickets without a live database connection.
""")

st.info("Tip: open **Theater Helper** from the sidebar to browse and download the SQL file from the app.")
