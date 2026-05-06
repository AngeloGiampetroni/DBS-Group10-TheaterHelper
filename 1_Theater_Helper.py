import os
import sys

import pandas as pd
import plotly.express as px
import streamlit as st

_PAGES_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PAGES_DIR not in sys.path:
    sys.path.insert(0, _PAGES_DIR)

import theater_data as td

st.set_page_config(
    page_title="Grand Marquee Cinemas",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

THEATER_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Outfit:wght@300;400;600&display=swap');
html, body, [class*="css"] { font-family: 'Outfit', sans-serif; }
h1, h2, h3, .marquee-text { font-family: 'Bebas Neue', sans-serif !important; letter-spacing: 0.06em; }
.stApp {
    background: radial-gradient(ellipse at 50% 0%, #2a1018 0%, #0c0c10 45%, #050508 100%) !important;
    color: #e8e4dc;
}
[data-testid="stHeader"] { background: rgba(12, 8, 10, 0.95) !important; border-bottom: 1px solid #5c1a1a; }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a0a0e 0%, #0d080a 100%) !important;
    border-right: 1px solid #3d1518 !important;
}
[data-testid="stSidebar"] * { color: #e0d8ce !important; }
.block-container { padding-top: 1.2rem !important; max-width: 1200px; }
div[data-testid="stExpander"] { background: rgba(30, 12, 16, 0.6); border: 1px solid #4a2028; border-radius: 8px; }
.stTabs [data-baseweb="tab-list"] { gap: 8px; background: rgba(0,0,0,0.25); padding: 8px; border-radius: 8px; }
.stTabs [data-baseweb="tab"] { background: #2a1218; border: 1px solid #5c2a32; color: #f0e6dc; border-radius: 6px; }
.marquee-outer {
    overflow: hidden;
    background: linear-gradient(90deg, #3d080c, #6b1018, #3d080c);
    border: 3px solid #c9a227;
    border-radius: 4px;
    box-shadow: 0 0 24px rgba(201, 162, 39, 0.25), inset 0 0 40px rgba(0,0,0,0.5);
    margin-bottom: 1.5rem;
    padding: 0.5rem 0;
}
.marquee-inner {
    display: inline-block;
    white-space: nowrap;
    animation: marquee 28s linear infinite;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.75rem;
    color: #ffe9a8;
    text-shadow: 0 0 12px rgba(255, 200, 100, 0.6);
    letter-spacing: 0.12em;
    padding-left: 100%;
}
@keyframes marquee {
    0% { transform: translateX(0); }
    100% { transform: translateX(-100%); }
}
.poster-row { display: flex; flex-wrap: wrap; gap: 12px; justify-content: center; margin: 1rem 0; }
.poster {
    width: 140px;
    min-height: 200px;
    background: linear-gradient(160deg, #2a151c 0%, #0f0608 100%);
    border: 2px solid #8b6914;
    border-radius: 6px;
    padding: 12px 10px;
    text-align: center;
    box-shadow: 0 8px 24px rgba(0,0,0,0.5);
}
.poster-title { font-family: 'Bebas Neue', sans-serif; font-size: 1.15rem; color: #ffd56a; line-height: 1.1; margin-bottom: 6px; }
.poster-meta { font-size: 0.72rem; color: #b8a99a; line-height: 1.35; }
.screen-glow {
    margin: 2rem auto 1rem;
    max-width: 720px;
    height: 8px;
    background: linear-gradient(90deg, transparent, rgba(120, 180, 255, 0.35), transparent);
    border-radius: 50%;
    filter: blur(6px);
}
"""

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

movies_df = td.load_movies()
schedule_df = td.schedule_with_movies()
tickets_df = td.tickets_with_details()


@st.cache_data
def ticket_sales_by_movie() -> pd.DataFrame:
    t = td.load_tickets().rename(columns={"id": "ticket_id"})
    m = td.load_movies().rename(columns={"id": "movie_id"})
    merged = t.merge(m, left_on="movie", right_on="movie_id")
    g = merged.groupby("title", as_index=False).agg(
        sold=("ticket_id", "count"),
        revenue=("price", "sum"),
    )
    return g.sort_values("sold", ascending=False)


@st.cache_data
def revenue_by_genre() -> pd.DataFrame:
    t = td.load_tickets().rename(columns={"id": "ticket_id"})
    m = td.load_movies().rename(columns={"id": "movie_id"})
    merged = t.merge(m, left_on="movie", right_on="movie_id")
    return merged.groupby("genre", as_index=False).agg(
        revenue=("price", "sum"),
        tickets=("ticket_id", "count"),
    )


with st.sidebar:
    st.markdown("### Concessions & filters")
    st.markdown("---")
    date_opts = ["All dates"] + sorted(schedule_df["date"].unique().tolist())
    pick_date = st.selectbox("Showtime date", date_opts)
    genre_filter = st.multiselect(
        "Genres on screen",
        options=sorted(movies_df["genre"].unique()),
        default=sorted(movies_df["genre"].unique()),
    )
    st.markdown("---")
    st.markdown(
        "<small>Velvet seats • digital projection • hearing-assisted devices available</small>",
        unsafe_allow_html=True,
    )

filt_schedule = schedule_df[schedule_df["genre"].isin(genre_filter)]
if pick_date != "All dates":
    filt_schedule = filt_schedule[filt_schedule["date"] == pick_date]

tab_show, tab_films, tab_box, tab_sql = st.tabs(
    ["Showtimes", "Now playing wall", "Box office", "TheaterHelperDB.sql"]
)

with tab_show:
    st.subheader("This week's screenings")
    st.markdown('<div class="screen-glow"></div>', unsafe_allow_html=True)
    disp = filt_schedule.copy()
    disp["time"] = disp["time"].astype(str).str.slice(0, 5)
    st.dataframe(
        disp,
        use_container_width=True,
        hide_index=True,
        column_config={
            "showing_id": st.column_config.NumberColumn("ID", width="small"),
            "title": st.column_config.TextColumn("Feature", width="medium"),
            "genre": st.column_config.TextColumn("Genre"),
            "age_rating": st.column_config.TextColumn("Rated"),
            "runtime": st.column_config.TextColumn("Runtime"),
            "studio": st.column_config.TextColumn("Studio", width="medium"),
            "room_number": st.column_config.TextColumn("Auditorium"),
            "date": st.column_config.TextColumn("Date"),
            "time": st.column_config.TextColumn("Start"),
        },
    )

with tab_films:
    st.subheader("Lobby poster wall")
    mview = movies_df[movies_df["genre"].isin(genre_filter)].reset_index(drop=True)
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
    sales = ticket_sales_by_movie()
    genre_rev = revenue_by_genre()

    fig_bar = px.bar(
        sales,
        x="title",
        y="sold",
        color="sold",
        color_continuous_scale=["#3d1518", "#c9a227"],
        template="plotly_dark",
        title="Tickets sold per title",
    )
    fig_bar.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(20,10,14,0.8)",
        font=dict(color="#e8e4dc"),
        xaxis_tickangle=-35,
        showlegend=False,
        margin=dict(b=120),
    )
    fig_bar.update_traces(marker_line_width=0)

    fig_pie = px.pie(
        genre_rev,
        values="revenue",
        names="genre",
        hole=0.45,
        template="plotly_dark",
        title="Revenue mix by genre",
        color_discrete_sequence=px.colors.sequential.YlOrRd_r,
    )
    fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#e8e4dc"))

    with col1:
        st.plotly_chart(fig_bar, use_container_width=True)
    with col2:
        st.plotly_chart(fig_pie, use_container_width=True)

    st.dataframe(
        tickets_df[tickets_df["genre"].isin(genre_filter)],
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
        "Download or preview the same `INSERT` data used on this site. "
        "Run against your `theater` schema (tables: `movie`, `customer`, `showing`, `ticket`)."
    )
    sql_text = td.read_sql_file()
    st.download_button(
        label="Download TheaterHelperDB.sql",
        data=sql_text,
        file_name="TheaterHelperDB.sql",
        mime="text/plain",
    )
    with st.expander("View SQL in the browser"):
        st.code(sql_text, language="sql")

st.markdown('<div class="screen-glow"></div>', unsafe_allow_html=True)
st.caption("Enjoy the show — thank you for visiting Grand Marquee Cinemas.")
