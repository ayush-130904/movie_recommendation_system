import requests
import streamlit as st

# =============================
# CONFIG
# =============================
API_BASE = "https://cinematch-api-gxu6.onrender.com" or "http://127.0.0.1:8000"
TMDB_IMG = "https://image.tmdb.org/t/p/w500"

st.set_page_config(page_title="CineMatch", page_icon="🎬", layout="wide")

# =============================
# STYLES — Cinematic Dark Theme
# =============================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Root & Body ── */
:root {
  --bg:       #0a0a0f;
  --surface:  #111118;
  --surface2: #1a1a26;
  --border:   rgba(255,255,255,0.07);
  --gold:     #f5c518;
  --gold-dim: rgba(245,197,24,0.15);
  --text:     #e8e8f0;
  --muted:    #7a7a99;
  --red:      #e05252;
}

html, body, [data-testid="stAppViewContainer"] {
  background-color: var(--bg) !important;
  color: var(--text) !important;
  font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stAppViewContainer"] {
  background:
    radial-gradient(ellipse 80% 40% at 50% -10%, rgba(245,197,24,0.06) 0%, transparent 70%),
    var(--bg) !important;
}

/* ── Streamlit Top Toolbar / Header ── */
[data-testid="stHeader"],
header[data-testid="stHeader"] {
  background: var(--bg) !important;
  border-bottom: 1px solid var(--border) !important;
}
[data-testid="stToolbar"],
[data-testid="stDecoration"] {
  background: var(--bg) !important;
}
/* Hide the red decoration bar at top */
[data-testid="stDecoration"] { display: none !important; }

/* ── Block Container ── */
.block-container {
  padding-top: 1.5rem !important;
  padding-bottom: 3rem !important;
  max-width: 1440px !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: var(--surface) !important;
  border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label { color: var(--muted) !important; font-size: 0.78rem !important; text-transform: uppercase; letter-spacing: 0.08em; }

/* Sidebar selectbox & slider */
[data-testid="stSidebar"] [data-baseweb="select"] > div {
  background: var(--surface2) !important;
  border: 1px solid var(--border) !important;
  border-radius: 8px !important;
  color: var(--text) !important;
}
[data-baseweb="popover"] { background: var(--surface2) !important; }
[data-baseweb="menu"] { background: var(--surface2) !important; }
[data-baseweb="option"] { color: var(--text) !important; }
[data-baseweb="option"]:hover { background: var(--gold-dim) !important; }

/* ── Sidebar Home Button ── */
[data-testid="stSidebar"] .stButton > button {
  width: 100%;
  background: var(--gold-dim) !important;
  border: 1px solid rgba(245,197,24,0.3) !important;
  color: var(--gold) !important;
  border-radius: 8px !important;
  font-weight: 600 !important;
  font-size: 0.85rem !important;
  letter-spacing: 0.04em;
  transition: all 0.2s ease !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
  background: rgba(245,197,24,0.28) !important;
  border-color: var(--gold) !important;
}

/* ── Main Buttons ── */
.stButton > button {
  background: transparent !important;
  border: 1px solid var(--border) !important;
  color: var(--muted) !important;
  border-radius: 6px !important;
  font-size: 0.72rem !important;
  padding: 4px 10px !important;
  transition: all 0.18s ease !important;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  font-weight: 500 !important;
}
.stButton > button:hover {
  background: var(--gold-dim) !important;
  border-color: var(--gold) !important;
  color: var(--gold) !important;
}

/* ── Text Input ── */
.stTextInput > div > div > input {
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
  color: var(--text) !important;
  font-size: 1rem !important;
  padding: 14px 18px !important;
  transition: border 0.2s;
}
.stTextInput > div > div > input:focus {
  border-color: var(--gold) !important;
  box-shadow: 0 0 0 3px rgba(245,197,24,0.12) !important;
}
.stTextInput label { color: var(--muted) !important; font-size: 0.78rem !important; text-transform: uppercase; letter-spacing: 0.08em; }

/* ── Selectbox (suggestions dropdown) ── */
[data-baseweb="select"] > div {
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
  color: var(--text) !important;
}

/* ── Divider ── */
hr { border-color: var(--border) !important; margin: 1.2rem 0 !important; }

/* ── Headings ── */
h1 { font-family: 'Bebas Neue', sans-serif !important; font-size: 3rem !important; letter-spacing: 0.06em !important; color: var(--text) !important; margin-bottom: 0 !important; }
h2 { font-family: 'Bebas Neue', sans-serif !important; letter-spacing: 0.05em !important; color: var(--text) !important; }
h3 { font-size: 1rem !important; font-weight: 600 !important; color: var(--text) !important; text-transform: uppercase; letter-spacing: 0.08em; }
h4 { font-size: 0.82rem !important; font-weight: 500 !important; color: var(--muted) !important; text-transform: uppercase; letter-spacing: 0.12em; }

/* ── Info / Warning / Error boxes ── */
.stAlert { background: var(--surface2) !important; border-left-color: var(--gold) !important; color: var(--text) !important; border-radius: 8px !important; }

/* ── Custom components ── */
.site-header {
  display: flex;
  align-items: baseline;
  gap: 14px;
  padding: 2rem 0 0.4rem;
  border-bottom: 1px solid var(--border);
  margin-bottom: 1.6rem;
}
.site-logo {
  font-family: 'Bebas Neue', sans-serif;
  font-size: 2.8rem;
  letter-spacing: 0.06em;
  color: #ffffff;
  line-height: 1;
  text-shadow: 0 2px 20px rgba(0,0,0,0.8);
}
.site-logo .cine { color: var(--gold); }
.site-logo .match { color: #ffffff; }
.site-tagline {
  color: var(--muted);
  font-size: 0.82rem;
  letter-spacing: 0.05em;
}

.section-label {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 1.6rem 0 1rem;
}
.section-label .pill {
  background: var(--gold);
  color: #0a0a0f;
  font-size: 0.68rem;
  font-weight: 700;
  padding: 3px 9px;
  border-radius: 20px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}
.section-label .label-text {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.movie-card {
  border: 1px solid var(--border);
  border-radius: 12px;
  overflow: hidden;
  background: var(--surface);
  transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
  cursor: pointer;
  position: relative;
}
.movie-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 40px rgba(0,0,0,0.5), 0 0 0 1px rgba(245,197,24,0.3);
  border-color: rgba(245,197,24,0.3);
}
.movie-card-inner { padding: 8px 10px 10px; }
.movie-title {
  font-size: 0.78rem;
  font-weight: 500;
  color: var(--text);
  line-height: 1.3;
  height: 2.1rem;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}
.movie-year {
  font-size: 0.68rem;
  color: var(--muted);
  margin-top: 3px;
}

.detail-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 24px;
}
.detail-title {
  font-family: 'Bebas Neue', sans-serif;
  font-size: 2.4rem;
  letter-spacing: 0.04em;
  color: var(--text);
  line-height: 1.05;
  margin-bottom: 10px;
}
.meta-row {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  margin-bottom: 14px;
}
.meta-chip {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 3px 12px;
  font-size: 0.73rem;
  color: var(--muted);
  letter-spacing: 0.04em;
}
.meta-chip.gold { background: var(--gold-dim); border-color: rgba(245,197,24,0.3); color: var(--gold); }
.overview-text {
  font-size: 0.9rem;
  line-height: 1.65;
  color: rgba(232,232,240,0.85);
}
.back-btn-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 1.4rem;
}
.small-muted { color: var(--muted); font-size: 0.85rem; }
.sidebar-brand {
  font-family: 'Bebas Neue', sans-serif;
  font-size: 1.6rem;
  letter-spacing: 0.08em;
  margin-bottom: 1rem;
}
.sidebar-brand .cine { color: var(--gold); }
.sidebar-brand .match { color: #ffffff; }
.sidebar-sep { border-color: var(--border) !important; margin: 0.8rem 0 !important; }
</style>
""", unsafe_allow_html=True)

# =============================
# STATE + ROUTING
# =============================
if "view" not in st.session_state:
    st.session_state.view = "home"
if "selected_tmdb_id" not in st.session_state:
    st.session_state.selected_tmdb_id = None

qp_view = st.query_params.get("view")
qp_id = st.query_params.get("id")
if qp_view in ("home", "details"):
    st.session_state.view = qp_view
if qp_id:
    try:
        st.session_state.selected_tmdb_id = int(qp_id)
        st.session_state.view = "details"
    except:
        pass


def goto_home():
    st.session_state.view = "home"
    st.query_params["view"] = "home"
    if "id" in st.query_params:
        del st.query_params["id"]
    st.rerun()


def goto_details(tmdb_id: int):
    st.session_state.view = "details"
    st.session_state.selected_tmdb_id = int(tmdb_id)
    st.query_params["view"] = "details"
    st.query_params["id"] = str(int(tmdb_id))
    st.rerun()


# =============================
# API HELPERS
# =============================
@st.cache_data(ttl=30)
def api_get_json(path: str, params: dict | None = None):
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=25)
        if r.status_code >= 400:
            return None, f"HTTP {r.status_code}: {r.text[:300]}"
        return r.json(), None
    except Exception as e:
        return None, f"Request failed: {e}"


def poster_grid(cards, cols=6, key_prefix="grid"):
    if not cards:
        st.info("No movies to show.")
        return

    rows = (len(cards) + cols - 1) // cols
    idx = 0
    for r in range(rows):
        colset = st.columns(cols, gap="small")
        for c in range(cols):
            if idx >= len(cards):
                break
            m = cards[idx]
            idx += 1

            tmdb_id = m.get("tmdb_id")
            title = m.get("title", "Untitled")
            poster = m.get("poster_url")

            with colset[c]:
                st.markdown("<div class='movie-card'>", unsafe_allow_html=True)
                if poster:
                    st.image(poster, use_column_width=True)
                else:
                    st.markdown(
                        "<div style='height:160px;display:flex;align-items:center;"
                        "justify-content:center;background:#1a1a26;color:#7a7a99;"
                        "font-size:2rem;'>🎬</div>",
                        unsafe_allow_html=True,
                    )
                st.markdown(
                    f"<div class='movie-card-inner'>"
                    f"<div class='movie-title'>{title}</div>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
                st.markdown("</div>", unsafe_allow_html=True)

                if st.button("▶ Open", key=f"{key_prefix}_{r}_{c}_{idx}_{tmdb_id}"):
                    if tmdb_id:
                        goto_details(tmdb_id)


def to_cards_from_tfidf_items(tfidf_items):
    cards = []

    for x in tfidf_items or []:
        tmdb = x.get("tmdb")

        cards.append({
            "tmdb_id": tmdb.get("tmdb_id") if tmdb else None,
            "title": (
                tmdb.get("title")
                if tmdb and tmdb.get("title")
                else x.get("title", "Untitled")
            ),
            "poster_url": (
                tmdb.get("poster_url")
                if tmdb
                else None
            ),
        })

    return cards


def parse_tmdb_search_to_cards(data, keyword: str, limit: int = 24):
    keyword_l = keyword.strip().lower()

    if isinstance(data, dict) and "results" in data:
        raw = data.get("results") or []
        raw_items = []
        for m in raw:
            title = (m.get("title") or "").strip()
            tmdb_id = m.get("id")
            poster_path = m.get("poster_path")
            if not title or not tmdb_id:
                continue
            raw_items.append({
                "tmdb_id": int(tmdb_id),
                "title": title,
                "poster_url": f"{TMDB_IMG}{poster_path}" if poster_path else None,
                "release_date": m.get("release_date", ""),
            })
    elif isinstance(data, list):
        raw_items = []
        for m in data:
            tmdb_id = m.get("tmdb_id") or m.get("id")
            title = (m.get("title") or "").strip()
            poster_url = m.get("poster_url")
            if not title or not tmdb_id:
                continue
            raw_items.append({
                "tmdb_id": int(tmdb_id),
                "title": title,
                "poster_url": poster_url,
                "release_date": m.get("release_date", ""),
            })
    else:
        return [], []

    matched = [x for x in raw_items if keyword_l in x["title"].lower()]
    final_list = matched if matched else raw_items

    suggestions = []
    for x in final_list[:10]:
        year = (x.get("release_date") or "")[:4]
        label = f"{x['title']} ({year})" if year else x["title"]
        suggestions.append((label, x["tmdb_id"]))

    cards = [
        {"tmdb_id": x["tmdb_id"], "title": x["title"], "poster_url": x["poster_url"]}
        for x in final_list[:limit]
    ]
    return suggestions, cards


# =============================
# SIDEBAR
# =============================
CATEGORY_ICONS = {
    "trending": "🔥",
    "popular": "⭐",
    "top_rated": "🏆",
    "now_playing": "🎞️",
    "upcoming": "📅",
}

with st.sidebar:
    st.markdown(
        "<div class='sidebar-brand'><span class='cine'>Cine</span><span class='match'>Match</span></div>",
        unsafe_allow_html=True,
    )
    if st.button("🏠  Home"):
        goto_home()

    st.markdown("<hr class='sidebar-sep'>", unsafe_allow_html=True)

    st.markdown(
        "<div style='color:#7a7a99;font-size:0.72rem;text-transform:uppercase;"
        "letter-spacing:0.1em;margin-bottom:6px;'>Feed Category</div>",
        unsafe_allow_html=True,
    )
    home_category = st.selectbox(
        "Category",
        ["trending", "popular", "top_rated", "now_playing", "upcoming"],
        index=0,
        label_visibility="collapsed",
    )
    st.markdown(
        "<div style='color:#7a7a99;font-size:0.72rem;text-transform:uppercase;"
        "letter-spacing:0.1em;margin-top:14px;margin-bottom:4px;'>Grid Columns</div>",
        unsafe_allow_html=True,
    )
    grid_cols = st.slider("Grid columns", 4, 8, 6, label_visibility="collapsed")

    st.markdown("<hr class='sidebar-sep'>", unsafe_allow_html=True)
    st.markdown(
        "<div style='color:#3d3d55;font-size:0.7rem;margin-top:8px;'>"
        "Powered by TMDB · TF-IDF</div>",
        unsafe_allow_html=True,
    )


# =============================
# HEADER
# =============================
st.markdown(
    "<div class='site-header'>"
    "<span class='site-logo'><span class='cine'>Cine</span><span class='match'>Match</span></span>"
    "<span class='site-tagline'>Your cinematic compass — discover, explore, recommend</span>"
    "</div>",
    unsafe_allow_html=True,
)


# ==========================================================
# VIEW: HOME
# ==========================================================
if st.session_state.view == "home":
    typed = st.text_input(
        "Search",
        placeholder="🔍  Search by title — avenger, batman, love...",
        label_visibility="collapsed",
    )

    if typed.strip():
        if len(typed.strip()) < 2:
            st.caption("Type at least 2 characters for suggestions.")
        else:
            data, err = api_get_json("/tmdb/search", params={"query": typed.strip()})

            if err or data is None:
                st.error(f"Search failed: {err}")
            else:
                suggestions, cards = parse_tmdb_search_to_cards(data, typed.strip(), limit=24)

                if suggestions:
                    labels = ["— Select a title —"] + [s[0] for s in suggestions]
                    selected = st.selectbox("Suggestions", labels, index=0, label_visibility="collapsed")

                    if selected != "— Select a title —":
                        label_to_id = {s[0]: s[1] for s in suggestions}
                        goto_details(label_to_id[selected])
                else:
                    st.info("No suggestions found. Try another keyword.")

                st.markdown(
                    "<div class='section-label'>"
                    "<span class='pill'>Results</span>"
                    f"<span class='label-text'>Matching &ldquo;{typed}&rdquo;</span>"
                    "</div>",
                    unsafe_allow_html=True,
                )
                poster_grid(cards, cols=grid_cols, key_prefix="search_results")

        st.stop()

    # HOME FEED
    icon = CATEGORY_ICONS.get(home_category, "🎬")
    label = home_category.replace("_", " ").title()
    st.markdown(
        f"<div class='section-label'>"
        f"<span class='pill'>{icon} {label}</span>"
        f"<span class='label-text'>Home Feed</span>"
        f"</div>",
        unsafe_allow_html=True,
    )

    home_cards, err = api_get_json("/home", params={"category": home_category, "limit": 24})
    if err or not home_cards:
        st.error(f"Home feed failed: {err or 'Unknown error'}")
        st.stop()

    poster_grid(home_cards, cols=grid_cols, key_prefix="home_feed")


# ==========================================================
# VIEW: DETAILS
# ==========================================================
elif st.session_state.view == "details":
    tmdb_id = st.session_state.selected_tmdb_id
    if not tmdb_id:
        st.warning("No movie selected.")
        if st.button("← Back to Home"):
            goto_home()
        st.stop()

    if st.button("← Back to Home"):
        goto_home()

    data, err = api_get_json(f"/movie/id/{tmdb_id}")
    if err or not data:
        st.error(f"Could not load details: {err or 'Unknown error'}")
        st.stop()

    # Backdrop (full-width cinematic banner)
    if data.get("backdrop_url"):
        st.markdown(
            f"<div style='border-radius:16px;overflow:hidden;margin-bottom:1.4rem;"
            f"position:relative;max-height:340px;'>"
            f"<img src='{data['backdrop_url']}' style='width:100%;object-fit:cover;"
            f"max-height:340px;opacity:0.75;display:block;'/>"
            f"<div style='position:absolute;inset:0;"
            f"background:linear-gradient(to right,rgba(10,10,15,0.85) 0%,transparent 60%);"
            f"border-radius:16px;'></div>"
            f"</div>",
            unsafe_allow_html=True,
        )

    left, right = st.columns([1, 2.6], gap="large")

    with left:
        if data.get("poster_url"):
            st.image(data["poster_url"], use_column_width=True)
        else:
            st.markdown(
                "<div style='height:320px;display:flex;align-items:center;"
                "justify-content:center;background:#1a1a26;border-radius:12px;"
                "color:#7a7a99;font-size:3rem;'>🎬</div>",
                unsafe_allow_html=True,
            )

    with right:
        st.markdown("<div class='detail-card'>", unsafe_allow_html=True)

        release = data.get("release_date") or ""
        year = release[:4] if release else ""
        genres = data.get("genres", []) or []
        genre_names = ", ".join([g["name"] for g in genres]) or "—"

        st.markdown(
            f"<div class='detail-title'>{data.get('title', '')}</div>",
            unsafe_allow_html=True,
        )

        chips_html = ""
        if year:
            chips_html += f"<span class='meta-chip gold'>{year}</span>"
        if release:
            chips_html += f"<span class='meta-chip'>{release}</span>"
        for g in genres:
            chips_html += f"<span class='meta-chip'>{g['name']}</span>"

        if chips_html:
            st.markdown(
                f"<div class='meta-row'>{chips_html}</div>",
                unsafe_allow_html=True,
            )

        st.markdown("<hr style='border-color:rgba(255,255,255,0.07);margin:12px 0;'>", unsafe_allow_html=True)
        st.markdown(
            "<div style='color:#7a7a99;font-size:0.72rem;text-transform:uppercase;"
            "letter-spacing:0.1em;margin-bottom:8px;'>Overview</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div class='overview-text'>{data.get('overview') or 'No overview available.'}</div>",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Recommendations ──
    st.markdown("<div style='height:1.6rem;'></div>", unsafe_allow_html=True)

    title = (data.get("title") or "").strip()
    if title:
        bundle, err2 = api_get_json(
            "/movie/search",
            params={"query": title, "tfidf_top_n": 12, "genre_limit": 12},
        )
      st.write("API Error:", err2)

      if bundle:
          st.write(
              "TFIDF Count:",
              len(bundle.get("tfidf_recommendations", []))
          )
      
          st.json(bundle.get("tfidf_recommendations", []))
      

        if not err2 and bundle:
            st.markdown(
                "<div class='section-label'>"
                "<span class='pill'>TF-IDF</span>"
                "<span class='label-text'>Similar Movies</span>"
                "</div>",
                unsafe_allow_html=True,
            )
            tfidf_cards = to_cards_from_tfidf_items(
                bundle.get("tfidf_recommendations", [])
            )
            
            st.write("Cards Count:", len(tfidf_cards))
            
            poster_grid(
                tfidf_cards,
                cols=grid_cols,
                key_prefix="details_tfidf",
            )

            st.markdown(
                "<div class='section-label'>"
                "<span class='pill'>Genre</span>"
                "<span class='label-text'>More Like This</span>"
                "</div>",
                unsafe_allow_html=True,
            )
            poster_grid(
                bundle.get("genre_recommendations", []),
                cols=grid_cols,
                key_prefix="details_genre",
            )
        else:
            st.info("Showing Genre recommendations (fallback).")
            genre_only, err3 = api_get_json(
                "/recommend/genre", params={"tmdb_id": tmdb_id, "limit": 18}
            )
            if not err3 and genre_only:
                poster_grid(genre_only, cols=grid_cols, key_prefix="details_genre_fallback")
            else:
                st.warning("No recommendations available right now.")
    else:
        st.warning("No title available to compute recommendations.")
