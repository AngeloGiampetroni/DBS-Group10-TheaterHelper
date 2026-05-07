
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