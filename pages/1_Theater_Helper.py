import os
import sys

import pandas as pd
import plotly.express as px
import streamlit as st
from database.database_helper import TheaterDBHelper
from theater_css import THEATER_CSS

st.set_page_config(
    page_title="Grand Marquee Cinemas",
    page_icon="🎬",
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

st.markdown(
    """
    <div class="marquee-outer"><div class="marquee-inner">
    NOW SHOWING &nbsp;•&nbsp; FRESH POPCORN &nbsp;•&nbsp; MILWAUKEE'S FINEST SCREENS
    &nbsp;•&nbsp; STARLIGHT RUN &nbsp;•&nbsp; ORBITFALL &nbsp;•&nbsp; STEEL HORIZON &nbsp;•&nbsp;
    TONIGHT ONLY — GET YOUR TICKETS &nbsp;•&nbsp;
    </div></div>
    """,
    unsafe_allow_html=True,
)

st.markdown("# Grand Marquee Cinemas")
st.caption("Your showtimes, films, and ticket desk — powered by the same data as `TheaterHelperDB.sql`.")


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

tab_show, tab_films, tab_box, tab_sql = st.tabs(
    ["Showtimes", "Now playing wall", "Box office", "TheaterHelperDB.sql"]
)

with tab_show:
    st.subheader("This week's screenings")
    st.markdown('<div class="screen-glow"></div>', unsafe_allow_html=True)
    st.dataframe(
        db.get_query(
            "Select id, movie, room_number as 'room number', date, time from showing"
            ),
        use_container_width=True,
        hide_index=True,
    )

with tab_films:
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

with tab_box:
    st.subheader("Ticket sales from your dataset")
    col1, col2 = st.columns(2)
    sales = db.ticket_sales_by_movie()
    genre_rev = db.revenue_by_genre()

    st.dataframe(
        #tickets_df[tickets_df["genre"].isin(genre_filter)],
        db.get_tickets_with_filters(genre=genre_filter if genre_filter else None),
        use_container_width=True,
        hide_index=True,
        column_config={
            "ticket_id": st.column_config.NumberColumn("Ticket"),
            "customer_name": st.column_config.TextColumn("Guest"),
            "title": st.column_config.TextColumn("Film"),
            "genre": st.column_config.TextColumn("Genre"),
            "price": st.column_config.NumberColumn("Price", format="$%.2f"),
            "room_number": st.column_config.TextColumn("Room"),
            "date": st.column_config.TextColumn("Show date"),
            "time": st.column_config.TextColumn("Show time"),
        },
    )

with tab_sql:
    st.subheader("Database seed file")
    st.markdown(
        "Data used on this site."
    )
    st.download_button(
        label="Download TheaterHelperDB.sql",
        data=open(os.path.join(_PAGES_DIR, "TheaterHelperDB.sql"), "r").read(),
        file_name="TheaterHelperDB.sql",
        mime="text/plain",
    )
    st.download_button(
        label="Download TheaterHelperDB TABLES.sql",
        data=open(os.path.join(_PAGES_DIR, "TheaterHelperDB TABLES.sql"), "r").read(),
        file_name="TheaterHelperDB TABLES.sql",
        mime="text/plain",
    )
    with st.expander("View Our Mock SQL DATA"):
        st.code(open(os.path.join(_PAGES_DIR, "TheaterHelperDB.sql"), "r").read(), language="sql")
    with st.expander("Database schema reference"):
        st.code(open(os.path.join(_PAGES_DIR, "TheaterHelperDB TABLES.sql"), "r").read(), language="sql")

st.markdown('<div class="screen-glow"></div>', unsafe_allow_html=True)
st.caption("Enjoy the show — thank you for visiting Grand Marquee Cinemas.")
