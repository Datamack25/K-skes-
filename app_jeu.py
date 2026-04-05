"""
⚡ Quiz Master Pro v3
- CSV illimités (500+ lignes supportées, auto-détection de colonnes)
- Multijoueur partageable : code de salle unique, chaque joueur sur son propre appareil
- Timer par niveau, 4 niveaux de difficulté, 10 catégories
"""

import streamlit as st
import pandas as pd
import random
import time
import os
import json
import hashlib
from datetime import datetime, timedelta
import glob

# ══════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="⚡ Quiz Master Pro",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════
#  CSS
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&display=swap');

html,body,[class*="css"]{font-family:'Rajdhani',sans-serif;}
.stApp{
  background:radial-gradient(ellipse at top,#0d1b3e 0%,#050510 60%);
  min-height:100vh;
}
[data-testid="stSidebar"]{background:#070718;border-right:1px solid #00d4ff18;}

/* ── Title ── */
.main-title{
  font-family:'Orbitron',monospace;font-size:2.5rem;font-weight:900;
  text-align:center;
  background:linear-gradient(90deg,#00d4ff,#ff00ff,#00ff88,#ffaa00,#00d4ff);
  background-size:400%;
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  animation:gs 5s ease infinite;margin-bottom:0.1rem;
}
@keyframes gs{0%,100%{background-position:0%}50%{background-position:100%}}
.subtitle{
  text-align:center;color:#00d4ff66;
  font-size:0.78rem;letter-spacing:4px;text-transform:uppercase;margin-bottom:1.2rem;
}

/* ── Cards ── */
.card{
  background:linear-gradient(135deg,rgba(0,212,255,.04),rgba(255,0,255,.03));
  border:1px solid rgba(0,212,255,.22);border-radius:16px;
  padding:1.4rem;margin:.6rem 0;
  box-shadow:0 0 18px rgba(0,212,255,.06),inset 0 0 18px rgba(0,0,0,.25);
}
.q-card{
  background:linear-gradient(135deg,rgba(0,212,255,.07),rgba(0,0,0,.55));
  border:1px solid rgba(0,212,255,.5);border-radius:14px;
  padding:1.8rem;text-align:center;margin:1rem 0;
  box-shadow:0 0 28px rgba(0,212,255,.14);
}
.q-prompt{
  font-family:'Orbitron',monospace;font-size:1rem;color:#b0d8ff;
  letter-spacing:1px;margin-bottom:.5rem;
}
.q-term{
  font-family:'Orbitron',monospace;font-size:1.5rem;font-weight:900;
  color:#00ff88;text-shadow:0 0 22px rgba(0,255,136,.55);
  letter-spacing:2px;line-height:1.4;margin:.6rem 0;
}

/* ── Timer ── */
.timer{
  text-align:center;padding:.5rem 1.1rem;border-radius:50px;
  display:inline-block;font-family:'Orbitron',monospace;
  font-size:1.3rem;font-weight:900;
}
.t-green{background:rgba(0,255,136,.08);border:2px solid #00ff88;color:#00ff88;box-shadow:0 0 18px rgba(0,255,136,.25);}
.t-yellow{background:rgba(255,170,0,.08);border:2px solid #ffaa00;color:#ffaa00;box-shadow:0 0 18px rgba(255,170,0,.25);}
.t-red{background:rgba(255,50,50,.1);border:2px solid #ff4444;color:#ff4444;
  box-shadow:0 0 22px rgba(255,68,68,.35);animation:blink .5s infinite;}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.25}}

/* ── Notifications ── */
.notif{border-radius:14px;padding:1.4rem;text-align:center;margin:1rem 0;}
.n-ok{background:linear-gradient(135deg,rgba(0,255,136,.1),rgba(0,180,80,.05));
  border:2px solid #00ff88;box-shadow:0 0 45px rgba(0,255,136,.3),0 0 90px rgba(0,255,136,.08);
  animation:popIn .4s cubic-bezier(.34,1.56,.64,1);}
.n-wrong{background:linear-gradient(135deg,rgba(255,50,50,.1),rgba(180,0,0,.05));
  border:2px solid #ff4444;box-shadow:0 0 45px rgba(255,68,68,.3),0 0 90px rgba(255,68,68,.08);
  animation:shake .45s ease;}
.n-time{background:linear-gradient(135deg,rgba(255,170,0,.1),rgba(180,80,0,.05));
  border:2px solid #ffaa00;box-shadow:0 0 45px rgba(255,170,0,.3);
  animation:popIn .4s ease;}
@keyframes popIn{0%{transform:scale(.7);opacity:0}80%{transform:scale(1.04)}100%{transform:scale(1);opacity:1}}
@keyframes shake{0%,100%{transform:translateX(0)}20%{transform:translateX(-9px)}40%{transform:translateX(9px)}60%{transform:translateX(-6px)}80%{transform:translateX(6px)}}
.notif h2{font-family:'Orbitron',monospace;font-size:1.4rem;margin:0;}
.n-ok h2{color:#00ff88;text-shadow:0 0 18px #00ff88;}
.n-wrong h2{color:#ff4444;text-shadow:0 0 18px #ff4444;}
.n-time h2{color:#ffaa00;text-shadow:0 0 18px #ffaa00;}
.notif p{color:#ccc;font-size:.92rem;margin:.4rem 0 0;}

/* ── Score ── */
.score-box{
  background:linear-gradient(135deg,rgba(255,170,0,.1),rgba(255,0,255,.04));
  border:1px solid rgba(255,170,0,.38);border-radius:12px;
  padding:.9rem;text-align:center;margin-bottom:.9rem;
}
.score-box h3{color:#ffaa00;font-family:'Orbitron',monospace;font-size:.75rem;margin:0;}
.score-box .big{color:#fff;font-family:'Orbitron',monospace;font-size:1.9rem;font-weight:900;}

/* ── Players ── */
.p-row{
  display:flex;align-items:center;gap:.7rem;
  background:rgba(0,212,255,.04);border:1px solid rgba(0,212,255,.18);
  border-radius:10px;padding:.6rem .9rem;margin:.3rem 0;
}
.p-dot{width:12px;height:12px;border-radius:50%;flex-shrink:0;}
.p-name{color:#fff;font-weight:600;flex:1;font-size:.9rem;}
.p-score{color:#ffaa00;font-family:'Orbitron',monospace;font-weight:700;}
.p-active{border-color:#00ff88 !important;box-shadow:0 0 12px rgba(0,255,136,.18);}

/* ── Room badge ── */
.room-badge{
  background:rgba(0,212,255,.08);border:1px solid rgba(0,212,255,.4);
  border-radius:10px;padding:.7rem 1.2rem;text-align:center;
  font-family:'Orbitron',monospace;letter-spacing:3px;
}
.room-code{font-size:2rem;font-weight:900;color:#00d4ff;
  text-shadow:0 0 20px rgba(0,212,255,.6);}
.room-label{font-size:.65rem;color:#00d4ff77;letter-spacing:4px;text-transform:uppercase;}

/* ── Final ── */
.final{
  background:linear-gradient(135deg,rgba(0,212,255,.07),rgba(255,0,255,.04));
  border:2px solid rgba(0,212,255,.38);border-radius:20px;
  padding:2.4rem;text-align:center;
  box-shadow:0 0 55px rgba(0,212,255,.14);animation:popIn .7s ease;
}
.final h1{font-family:'Orbitron',monospace;color:#00ff88;font-size:1.9rem;
  text-shadow:0 0 25px #00ff88;margin-bottom:.4rem;}
.f-score{font-family:'Orbitron',monospace;font-size:3.2rem;font-weight:900;
  color:#ffaa00;text-shadow:0 0 35px #ffaa00;}

/* ── Buttons ── */
.stButton>button{
  width:100%;padding:.8rem 1rem;
  font-family:'Rajdhani',sans-serif;font-size:.98rem;font-weight:600;
  border-radius:10px;border:1px solid rgba(0,212,255,.32);
  background:linear-gradient(135deg,rgba(0,212,255,.07),rgba(0,0,0,.5));
  color:#dff0ff;cursor:pointer;transition:all .2s ease;
}
.stButton>button:hover{
  background:linear-gradient(135deg,rgba(0,212,255,.17),rgba(255,0,255,.07));
  border-color:#00d4ff;color:#fff;
  box-shadow:0 0 18px rgba(0,212,255,.3),0 0 36px rgba(0,212,255,.08);
  transform:translateY(-2px);
}

/* ── Misc ── */
.hdr{color:#00d4ff;font-size:.72rem;letter-spacing:3px;text-transform:uppercase;
  border-bottom:1px solid rgba(0,212,255,.2);padding-bottom:.25rem;margin:1.1rem 0 .7rem;}
.p-tag{text-align:center;font-family:'Orbitron',monospace;color:#ffaa00;
  font-size:.78rem;letter-spacing:2px;padding:.4rem;
  border-bottom:1px solid rgba(255,170,0,.22);margin-bottom:.7rem;}
.stTextInput>div>div>input{
  background:rgba(0,212,255,.04);border:1px solid rgba(0,212,255,.28);
  color:white;border-radius:8px;
}
#MainMenu,footer,header{visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  PATHS & CONSTANTS
# ══════════════════════════════════════════════════════════════
BASE      = os.path.dirname(os.path.abspath(__file__))
DATA_DIR  = os.path.join(BASE, "data")
ROOMS_DIR = os.path.join(BASE, "rooms")
os.makedirs(ROOMS_DIR, exist_ok=True)

PLAYER_COLORS = ["#00d4ff", "#ff00ff", "#00ff88", "#ffaa00"]
PLAYER_EMOJIS = ["🔵", "🟣", "🟢", "🟡"]

LEVELS = {
    "🌱 Débutant":  {"key":"debutant",  "time":30, "qs":10, "color":"#00d4ff", "mult":1},
    "⚡ Potentiel": {"key":"potentiel", "time":20, "qs":15, "color":"#00ff88", "mult":2},
    "🔥 Légende":   {"key":"legende",   "time":15, "qs":20, "color":"#ffaa00", "mult":3},
    "👑 Superstar": {"key":"superstar", "time":10, "qs":25, "color":"#ff00ff", "mult":5},
}

# ── CSV column schemas.  Each entry: (question_col, answer_col, prompt, type)
# type: "vocab" | "mcq" (has Choix_2/3/4 columns) | "music"
MODES = {
    "🔐 Sécurité Financière": {
        "file":"securite_financiere.csv","type":"vocab",
        "col_q":"Terme","col_a":"Definition",
        "prompt":"Quelle est la définition de :","color":"#00d4ff","icon":"🏦",
        "desc":"Vocabulaire AML/KYC/Compliance"
    },
    "🇫🇷 Français": {
        "file":"apprentissage_francais.csv","type":"vocab",
        "col_q":"Mot_Expression","col_a":"Definition_Synonyme",
        "prompt":"Synonyme ou définition de :","color":"#ff00ff","icon":"📚",
        "desc":"Vocabulaire & expressions françaises"
    },
    "🇬🇧 Anglais": {
        "file":"anglais.csv","type":"vocab",
        "col_q":"Mot_Expression","col_a":"Definition_EN",
        "prompt":"What is the definition of:","color":"#00ffff","icon":"🌐",
        "desc":"English vocabulary and idioms"
    },
    "🇪🇸 Espagnol": {
        "file":"espagnol.csv","type":"vocab",
        "col_q":"Mot_Expression","col_a":"Definition_ES",
        "prompt":"¿Cuál es la definición de:","color":"#ff6600","icon":"🌮",
        "desc":"Vocabulario y expresiones en español"
    },
    "🇭🇹 Créole Haïtien": {
        "file":"creole_haitien.csv","type":"vocab",
        "col_q":"Mot_Expression","col_a":"Definition_Kreyol",
        "prompt":"Ki definisyon oswa sinonim:","color":"#ff0044","icon":"🌴",
        "desc":"Mo ak ekspresyon an kreyòl ayisyen"
    },
    "🏛️ Monuments": {
        "file":"monuments_monde.csv","type":"vocab",
        "col_q":"Monument","col_a":"Pays",
        "prompt":"Dans quel pays se trouve :","color":"#ffaa00","icon":"🌍",
        "desc":"Monuments historiques du monde entier"
    },
    "🎵 Musique": {
        "file":"musique_monde.csv","type":"music",
        "col_q":"Artiste","col_a":"Chanson",
        "prompt":"Quelle est la chanson de :","color":"#ff00aa","icon":"🎶",
        "desc":"Artistes & chansons haïtiens et mondiaux"
    },
    "🔢 Mathématiques": {
        "file":"mathematiques.csv","type":"math",
        "col_q":"Question","col_a":"Reponse",
        "prompt":"Résolvez :","color":"#00ff88","icon":"🧮",
        "desc":"Algèbre et calcul — tous niveaux"
    },
    "🏺 Histoire": {
        "file":"histoire.csv","type":"mcq",
        "col_q":"Question","col_a":"Reponse_Correcte",
        "prompt":"","color":"#ff8800","icon":"📜",
        "desc":"France · Haïti · Histoire mondiale"
    },
    "🌐 Culture Générale": {
        "file":"culture_generale.csv","type":"mcq",
        "col_q":"Question","col_a":"Reponse_Correcte",
        "prompt":"","color":"#aa00ff","icon":"🧠",
        "desc":"Sciences · Géo · Art · Sports"
    },
}

# ══════════════════════════════════════════════════════════════
#  DATA LOADING  (unlimited rows — reads entire CSV)
# ══════════════════════════════════════════════════════════════
@st.cache_data(ttl=60)           # re-read every 60s so new rows appear after save
def load_csv(filename: str) -> pd.DataFrame:
    """Load any CSV from DATA_DIR without row limit.
    Handles: extra commas, BOM, mixed encodings, missing columns gracefully.
    """
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return pd.DataFrame()
    for enc in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            df = pd.read_csv(
                path,
                encoding=enc,
                on_bad_lines="skip",   # skip malformed rows instead of crashing
                dtype=str,             # read everything as string → no type errors
                skip_blank_lines=True,
            )
            df = df.loc[:, ~df.columns.str.startswith("Unnamed")]  # drop phantom cols
            df.columns = [c.strip() for c in df.columns]           # strip whitespace
            df = df.dropna(how="all")                               # remove empty rows
            return df
        except Exception:
            continue
    return pd.DataFrame()


def get_df(mode_name: str) -> pd.DataFrame:
    return load_csv(MODES[mode_name]["file"])


def csv_row_count(mode_name: str) -> int:
    return len(get_df(mode_name))


# ══════════════════════════════════════════════════════════════
#  QUESTION BUILDING  (supports any number of rows in CSV)
# ══════════════════════════════════════════════════════════════
def build_questions(mode_name: str, level_key: str, n: int) -> list:
    cfg = MODES[mode_name]
    df  = get_df(mode_name)

    if df.empty:
        return []

    # ── make sure required columns exist ──
    cq, ca = cfg["col_q"], cfg["col_a"]
    if cq not in df.columns or ca not in df.columns:
        st.error(f"⚠️ Colonnes manquantes dans {cfg['file']}: besoin de '{cq}' et '{ca}'.")
        return []

    df = df[[c for c in df.columns]].copy()
    df = df.dropna(subset=[cq, ca])
    df[cq] = df[cq].astype(str).str.strip()
    df[ca] = df[ca].astype(str).str.strip()
    df = df[df[cq] != ""].dropna()

    # ── level filter (math / mcq only) ──
    order = ["debutant", "potentiel", "legende", "superstar"]
    if cfg["type"] in ("math", "mcq") and "Difficulte" in df.columns:
        allowed = order[: order.index(level_key) + 1]
        sub = df[df["Difficulte"].isin(allowed)]
        df  = sub if len(sub) > 0 else df

    # ── shuffle & cap at n ──
    df = df.sample(frac=1, random_state=random.randint(0, 9999)).reset_index(drop=True)
    n  = min(n, len(df))
    if n == 0:
        return []

    qs = []
    for i in range(n):
        row   = df.iloc[i]
        right = str(row[ca]).strip()

        # ── build 4 choices ──
        if cfg["type"] == "mcq":
            choices = [right]
            for cx in ["Choix_2", "Choix_3", "Choix_4"]:
                if cx in df.columns:
                    v = str(row.get(cx, "")).strip()
                    if v and v != "nan" and v not in choices:
                        choices.append(v)
            # pad from pool if needed
            pool = df[df[ca] != right][ca].dropna().astype(str).str.strip()
            pool = pool[pool != "nan"].tolist()
            random.shuffle(pool)
            for p in pool:
                if len(choices) >= 4:
                    break
                if p not in choices:
                    choices.append(p)
            choices = choices[:4]
        else:
            pool = (
                df[df[ca] != right][ca]
                .dropna().astype(str).str.strip()
                .pipe(lambda s: s[s != "nan"])
                .tolist()
            )
            random.shuffle(pool)
            wrongs  = pool[:3]
            choices = [right] + wrongs

        random.shuffle(choices)

        qs.append({
            "question": str(row[cq]).strip(),
            "correct":  right,
            "choices":  choices,
            "prompt":   cfg["prompt"],
        })
    return qs


# ══════════════════════════════════════════════════════════════
#  ROOM SYSTEM  (file-based shared state for multiplayer)
# ══════════════════════════════════════════════════════════════
ROOM_TTL_MINUTES = 120   # rooms expire after 2h

def _room_path(code: str) -> str:
    return os.path.join(ROOMS_DIR, f"room_{code.upper()}.json")


def generate_room_code() -> str:
    base = hashlib.md5(str(time.time()).encode()).hexdigest()[:6].upper()
    return base


def room_create(code: str, host_name: str, mode: str, level: str):
    data = {
        "code": code,
        "host": host_name,
        "mode": mode,
        "level": level,
        "created": time.time(),
        "status": "waiting",   # waiting | playing | done
        "questions": [],
        "players": {host_name: {"score": 0, "q_index": 0, "done": False, "wrongs": []}},
        "cur_q_unlock": time.time(),   # timestamp when next q becomes available
    }
    _room_save(code, data)
    return data


def _room_save(code: str, data: dict):
    with open(_room_path(code), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def room_load(code: str) -> dict | None:
    p = _room_path(code)
    if not os.path.exists(p):
        return None
    try:
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
        # expire old rooms
        if time.time() - data.get("created", 0) > ROOM_TTL_MINUTES * 60:
            os.remove(p)
            return None
        return data
    except Exception:
        return None


def room_join(code: str, player_name: str) -> dict | None:
    data = room_load(code)
    if data is None:
        return None
    if player_name not in data["players"]:
        data["players"][player_name] = {"score": 0, "q_index": 0, "done": False, "wrongs": []}
        _room_save(code, data)
    return data


def room_answer(code: str, player_name: str, correct: bool, pts: int, wrong_entry=None):
    data = room_load(code)
    if data is None:
        return
    pl = data["players"].get(player_name, {"score": 0, "q_index": 0, "done": False, "wrongs": []})
    if correct:
        pl["score"] += pts
    elif wrong_entry:
        pl["wrongs"].append(wrong_entry)
    pl["q_index"] += 1
    total = len(data.get("questions", []))
    if pl["q_index"] >= total:
        pl["done"] = True
    data["players"][player_name] = pl
    _room_save(code, data)


def room_start(code: str, questions: list):
    data = room_load(code)
    if data is None:
        return
    data["status"]    = "playing"
    data["questions"] = questions
    _room_save(code, data)


def room_cleanup():
    """Remove expired room files."""
    for f in glob.glob(os.path.join(ROOMS_DIR, "room_*.json")):
        try:
            with open(f) as fp:
                d = json.load(fp)
            if time.time() - d.get("created", 0) > ROOM_TTL_MINUTES * 60:
                os.remove(f)
        except Exception:
            pass


# ══════════════════════════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════════════════════════
def _init():
    defaults = {
        "screen":       "home",       # home | solo | room_create | room_join | room_lobby | room_quiz | room_result | solo_quiz | solo_result
        "player_name":  "",
        "room_code":    "",
        # solo game
        "s_mode":       None,
        "s_level":      "🌱 Débutant",
        "s_questions":  [],
        "s_qi":         0,
        "s_score":      0,
        "s_wrongs":     [],
        "s_answered":   False,
        "s_correct":    None,
        "s_timeout":    False,
        "s_qtime":      None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init()


# ══════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════
def time_left_solo() -> int:
    if st.session_state.s_qtime is None:
        return 99
    lvl = LEVELS[st.session_state.s_level]
    return max(0, lvl["time"] - int(time.time() - st.session_state.s_qtime))


def time_left_room(room: dict) -> int:
    pname = st.session_state.player_name
    pl    = room["players"].get(pname, {})
    qi    = pl.get("q_index", 0)
    qtime = room.get(f"qtime_{pname}_{qi}")
    if qtime is None:
        return 99
    lvl = LEVELS.get(room.get("level", "🌱 Débutant"), LEVELS["🌱 Débutant"])
    return max(0, lvl["time"] - int(time.time() - qtime))


def badge(pct: int):
    if pct >= 90: return "🏆 LÉGENDAIRE", "#00ff88"
    if pct >= 70: return "⭐ EXPERT",     "#ffaa00"
    if pct >= 50: return "👍 BIEN",       "#00d4ff"
    return "📚 À REVOIR", "#ff4444"


def timer_html(tl: int, total_time: int) -> str:
    r = tl / total_time
    cls = "t-green" if r > .5 else ("t-yellow" if r > .25 else "t-red")
    return f'<div style="text-align:right"><div class="timer {cls}">⏱ {tl}s</div></div>'


def notif_html(kind: str, pts: int, correct_ans: str) -> str:
    if kind == "ok":
        return (f'<div class="notif n-ok"><h2>✅ CORRECT ! +{pts} pt{"s" if pts>1 else ""}</h2>'
                f'<p><strong style="color:#00ff88">{correct_ans}</strong></p></div>')
    elif kind == "wrong":
        return (f'<div class="notif n-wrong"><h2>❌ INCORRECT</h2>'
                f'<p>Bonne réponse : <strong style="color:#ff8888">{correct_ans}</strong></p></div>')
    else:
        return (f'<div class="notif n-time"><h2>⌛ TEMPS ÉCOULÉ !</h2>'
                f'<p>La réponse était : <strong style="color:#ffaa00">{correct_ans}</strong></p></div>')


# ══════════════════════════════════════════════════════════════
#  DEEP-LINK via query params
#  URL: ?room=ABCDEF  →  auto-redirect to join screen
# ══════════════════════════════════════════════════════════════
qp = st.query_params
if "room" in qp and st.session_state.screen == "home":
    st.session_state.room_code = qp["room"].upper()
    st.session_state.screen    = "room_join"
    st.rerun()


# ══════════════════════════════════════════════════════════════
#  SCREEN: HOME
# ══════════════════════════════════════════════════════════════
def screen_home():
    room_cleanup()
    st.markdown('<div class="main-title">⚡ QUIZ MASTER PRO</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">10 Catégories · 4 Niveaux · Solo & Multijoueur</div>', unsafe_allow_html=True)

    cl, cc, cr = st.columns([1, 3, 1])
    with cc:
        # Player name
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="hdr">👤 Votre nom</div>', unsafe_allow_html=True)
        name = st.text_input("", value=st.session_state.player_name,
                             placeholder="Entrez votre nom…",
                             label_visibility="collapsed", key="name_input")
        st.session_state.player_name = name.strip()
        st.markdown('</div>', unsafe_allow_html=True)

        # Mode buttons
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="hdr">🎮 Mode de jeu</div>', unsafe_allow_html=True)
        b1, b2, b3 = st.columns(3)
        with b1:
            if st.button("🎯 Solo", use_container_width=True):
                if not st.session_state.player_name:
                    st.warning("⚠️ Entrez votre nom !")
                else:
                    st.session_state.screen = "solo"
                    st.rerun()
        with b2:
            if st.button("🏠 Créer une salle", use_container_width=True):
                if not st.session_state.player_name:
                    st.warning("⚠️ Entrez votre nom !")
                else:
                    st.session_state.screen = "room_create"
                    st.rerun()
        with b3:
            if st.button("🔗 Rejoindre", use_container_width=True):
                if not st.session_state.player_name:
                    st.warning("⚠️ Entrez votre nom !")
                else:
                    st.session_state.screen = "room_join"
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Stats
    st.markdown("<br>", unsafe_allow_html=True)
    cols = st.columns(5)
    stats = [
        ("🔐","Finance","🔐 Sécurité Financière","#00d4ff"),
        ("🇫🇷","Français","🇫🇷 Français","#ff00ff"),
        ("🌍","Monuments","🏛️ Monuments","#ffaa00"),
        ("🎵","Musique","🎵 Musique","#ff00aa"),
        ("🧠","Culture","🌐 Culture Générale","#aa00ff"),
    ]
    for i,(icon,label,mname,color) in enumerate(stats):
        with cols[i]:
            n = csv_row_count(mname)
            st.markdown(
                f'<div class="card" style="text-align:center;padding:.9rem">'
                f'<div style="font-size:1.4rem">{icon}</div>'
                f'<div style="color:{color};font-family:Orbitron;font-size:.6rem;letter-spacing:2px">{label.upper()}</div>'
                f'<div style="color:#fff;font-size:1.1rem;font-weight:700">{n} entrées</div>'
                f'</div>', unsafe_allow_html=True
            )


# ══════════════════════════════════════════════════════════════
#  SCREEN: SOLO SETUP
# ══════════════════════════════════════════════════════════════
def screen_solo():
    st.markdown('<div class="main-title" style="font-size:1.8rem">🎯 Mode Solo</div>', unsafe_allow_html=True)

    cl, cc, cr = st.columns([1, 3, 1])
    with cc:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        # Level
        st.markdown('<div class="hdr">🎯 Niveau</div>', unsafe_allow_html=True)
        lc = st.columns(4)
        for i, (lname, lcfg) in enumerate(LEVELS.items()):
            with lc[i]:
                sel = st.session_state.s_level == lname
                bdr = "2px solid" if sel else "1px solid"
                bg  = "rgba(255,255,255,.05)" if sel else "transparent"
                key_cls = f"badge-{lcfg['key']}"
                st.markdown(
                    f'<div style="border:{bdr} {lcfg["color"]};background:{bg};border-radius:10px;'
                    f'padding:.5rem;text-align:center;color:{lcfg["color"]};'
                    f'font-family:Orbitron;font-size:.7rem;font-weight:700;letter-spacing:1px">'
                    f'{lname}<br><span style="opacity:.65;font-size:.6rem">⏱{lcfg["time"]}s · {lcfg["qs"]}Q · ×{lcfg["mult"]}</span>'
                    f'</div>', unsafe_allow_html=True
                )
                if st.button("", key=f"sl_{lname}", help=lname):
                    st.session_state.s_level = lname
                    st.rerun()

        # Mode
        st.markdown('<div class="hdr">🎮 Catégorie</div>', unsafe_allow_html=True)
        mc = st.columns(2)
        for mi, (mname, mcfg) in enumerate(MODES.items()):
            with mc[mi % 2]:
                c1, c2 = st.columns([3, 1])
                with c1:
                    n = csv_row_count(mname)
                    st.markdown(
                        f'<div style="color:{mcfg["color"]};font-weight:700;font-size:.95rem">'
                        f'{mcfg["icon"]} {mname.split(" ",1)[1]}</div>'
                        f'<div style="color:#777;font-size:.72rem">{mcfg["desc"]} · {n} entrées</div>',
                        unsafe_allow_html=True
                    )
                with c2:
                    if st.button("▶", key=f"ss_{mname}", use_container_width=True):
                        lvl = LEVELS[st.session_state.s_level]
                        qs  = build_questions(mname, lvl["key"], lvl["qs"])
                        if not qs:
                            st.error("CSV vide ou introuvable.")
                        else:
                            st.session_state.s_mode      = mname
                            st.session_state.s_questions = qs
                            st.session_state.s_qi        = 0
                            st.session_state.s_score     = 0
                            st.session_state.s_wrongs    = []
                            st.session_state.s_answered  = False
                            st.session_state.s_correct   = None
                            st.session_state.s_timeout   = False
                            st.session_state.s_qtime     = None
                            st.session_state.screen      = "solo_quiz"
                            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("← Retour", use_container_width=True):
            st.session_state.screen = "home"
            st.rerun()


# ══════════════════════════════════════════════════════════════
#  SCREEN: SOLO QUIZ
# ══════════════════════════════════════════════════════════════
def screen_solo_quiz():
    qs    = st.session_state.s_questions
    qi    = st.session_state.s_qi
    total = len(qs)
    lvl   = LEVELS[st.session_state.s_level]
    mode  = st.session_state.s_mode
    mcfg  = MODES[mode]

    if qi >= total:
        st.session_state.screen = "solo_result"
        st.rerun()
        return

    q = qs[qi]

    if st.session_state.s_qtime is None and not st.session_state.s_answered:
        st.session_state.s_qtime = time.time()

    tl = time_left_solo()
    if tl <= 0 and not st.session_state.s_answered:
        st.session_state.s_answered = True
        st.session_state.s_timeout  = True
        st.session_state.s_correct  = False
        st.session_state.s_wrongs.append({"question":q["question"],"votre_reponse":"⌛ Temps","bonne_reponse":q["correct"]})

    # sidebar
    with st.sidebar:
        st.markdown(f'<div class="p-tag">👤 {st.session_state.player_name.upper()}</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="score-box"><h3>⚡ SCORE</h3>'
            f'<div class="big">{st.session_state.s_score}</div></div>',
            unsafe_allow_html=True
        )
        lc = lvl["color"]
        st.markdown(
            f'<div style="padding:.7rem;background:rgba(0,0,0,.3);border:1px solid {lc}33;'
            f'border-radius:10px;text-align:center;margin-bottom:.7rem">'
            f'<div style="color:{lc};font-family:Orbitron;font-size:.7rem;letter-spacing:2px">'
            f'{st.session_state.s_level}</div>'
            f'<div style="color:#aaa;font-size:.75rem">Q {qi+1}/{total} · ×{lvl["mult"]} pts</div>'
            f'</div>', unsafe_allow_html=True
        )
        st.progress(qi / total)
        st.markdown("---")
        if st.button("🏠 Accueil"):
            st.session_state.screen = "home"
            st.rerun()

    # header row
    hc, tc = st.columns([3, 1])
    with hc:
        st.markdown(f'<div class="main-title" style="font-size:1.3rem;text-align:left">'
                    f'{mcfg["icon"]} {mode.split(" ",1)[1]}</div>', unsafe_allow_html=True)
    with tc:
        if not st.session_state.s_answered:
            st.markdown(timer_html(tl, lvl["time"]), unsafe_allow_html=True)

    st.progress(qi / total)
    st.markdown(f'<div style="text-align:center;color:#00d4ff55;font-size:.72rem;letter-spacing:2px">QUESTION {qi+1} / {total}</div>', unsafe_allow_html=True)

    # question
    st.markdown('<div class="q-card">', unsafe_allow_html=True)
    if q["prompt"]:
        st.markdown(f'<div class="q-prompt">{q["prompt"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="q-term">{q["question"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.s_answered:
        if st.session_state.s_timeout:
            kind = "time"
        elif st.session_state.s_correct:
            kind = "ok"
        else:
            kind = "wrong"
        st.markdown(notif_html(kind, lvl["mult"], q["correct"]), unsafe_allow_html=True)
        if st.button("➡️ Question suivante", use_container_width=True):
            st.session_state.s_qi      += 1
            st.session_state.s_answered = False
            st.session_state.s_correct  = None
            st.session_state.s_timeout  = False
            st.session_state.s_qtime    = None
            st.rerun()
    else:
        c1, c2 = st.columns(2)
        for idx, ch in enumerate(q["choices"]):
            with (c1 if idx % 2 == 0 else c2):
                if st.button(f"{'ABCD'[idx]}  {ch}", key=f"sa_{qi}_{idx}", use_container_width=True):
                    ok = (ch == q["correct"])
                    st.session_state.s_answered = True
                    st.session_state.s_correct  = ok
                    st.session_state.s_timeout  = False
                    if ok:
                        st.session_state.s_score += lvl["mult"]
                    else:
                        st.session_state.s_wrongs.append({"question":q["question"],"votre_reponse":ch,"bonne_reponse":q["correct"]})
                    st.rerun()
        if tl > 0:
            time.sleep(1)
            st.rerun()


# ══════════════════════════════════════════════════════════════
#  SCREEN: SOLO RESULT
# ══════════════════════════════════════════════════════════════
def screen_solo_result():
    lvl   = LEVELS[st.session_state.s_level]
    total = len(st.session_state.s_questions)
    score = st.session_state.s_score
    pct   = int(score / (total * lvl["mult"]) * 100) if total else 0
    bdg, bc = badge(pct)

    with st.sidebar:
        if st.button("🏠 Accueil"):
            st.session_state.screen = "home"
            st.rerun()
        if st.button("🔄 Rejouer"):
            qs = build_questions(st.session_state.s_mode, lvl["key"], lvl["qs"])
            st.session_state.s_questions = qs
            st.session_state.s_qi = 0; st.session_state.s_score = 0
            st.session_state.s_wrongs = []; st.session_state.s_answered = False
            st.session_state.s_correct = None; st.session_state.s_timeout = False
            st.session_state.s_qtime = None; st.session_state.screen = "solo_quiz"
            st.rerun()

    cl, cc, cr = st.columns([1, 3, 1])
    with cc:
        st.markdown(f"""
        <div class="final">
          <h1>🎯 RÉSULTATS</h1>
          <div style="color:#00d4ff88;font-family:Orbitron;font-size:.75rem;letter-spacing:3px">{st.session_state.player_name.upper()}</div>
          <div class="f-score">{score} pts</div>
          <div style="font-size:1.1rem;margin:.2rem">{pct}%</div>
          <div style="color:{bc};font-family:Orbitron;font-size:1.1rem;font-weight:700;
                       text-shadow:0 0 18px {bc};margin:.7rem 0">{bdg}</div>
          <div style="color:#555;font-size:.8rem">{st.session_state.s_mode} · {st.session_state.s_level}</div>
        </div>""", unsafe_allow_html=True)

        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            good = score // lvl["mult"]
            st.markdown(f'<div class="card" style="text-align:center"><div style="font-size:1.3rem">✅</div>'
                        f'<div style="color:#00ff88;font-family:Orbitron;font-size:.65rem">BONNES</div>'
                        f'<div style="color:#fff;font-size:1.2rem;font-weight:700">{good}</div></div>', unsafe_allow_html=True)
        with sc2:
            st.markdown(f'<div class="card" style="text-align:center"><div style="font-size:1.3rem">📊</div>'
                        f'<div style="color:#00d4ff;font-family:Orbitron;font-size:.65rem">TOTAL</div>'
                        f'<div style="color:#fff;font-size:1.2rem;font-weight:700">{total}</div></div>', unsafe_allow_html=True)
        with sc3:
            st.markdown(f'<div class="card" style="text-align:center"><div style="font-size:1.3rem">❌</div>'
                        f'<div style="color:#ff4444;font-family:Orbitron;font-size:.65rem">ERREURS</div>'
                        f'<div style="color:#fff;font-size:1.2rem;font-weight:700">{len(st.session_state.s_wrongs)}</div></div>', unsafe_allow_html=True)

        if st.session_state.s_wrongs:
            st.markdown('<div class="hdr">📖 Révision</div>', unsafe_allow_html=True)
            for wa in st.session_state.s_wrongs[:15]:
                st.markdown(f"""
                <div style="background:rgba(255,68,68,.04);border:1px solid rgba(255,68,68,.18);
                  border-radius:8px;padding:.65rem .9rem;margin:.25rem 0">
                  <div style="color:#00d4ff;font-weight:700;font-size:.88rem">{wa['question']}</div>
                  <div style="color:#ff8888;font-size:.78rem">Votre réponse : {wa['votre_reponse']}</div>
                  <div style="color:#00ff88;font-size:.78rem">✅ {wa['bonne_reponse']}</div>
                </div>""", unsafe_allow_html=True)

        br1, br2 = st.columns(2)
        with br1:
            if st.button("🔄 Rejouer", use_container_width=True):
                qs = build_questions(st.session_state.s_mode, lvl["key"], lvl["qs"])
                st.session_state.s_questions=qs; st.session_state.s_qi=0
                st.session_state.s_score=0; st.session_state.s_wrongs=[]
                st.session_state.s_answered=False; st.session_state.s_correct=None
                st.session_state.s_timeout=False; st.session_state.s_qtime=None
                st.session_state.screen="solo_quiz"; st.rerun()
        with br2:
            if st.button("🏠 Menu", use_container_width=True):
                st.session_state.screen = "home"; st.rerun()


# ══════════════════════════════════════════════════════════════
#  SCREEN: CREATE ROOM
# ══════════════════════════════════════════════════════════════
def screen_room_create():
    st.markdown('<div class="main-title" style="font-size:1.8rem">🏠 Créer une salle</div>', unsafe_allow_html=True)

    cl, cc, cr = st.columns([1, 3, 1])
    with cc:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        if "new_room_code" not in st.session_state:
            st.session_state.new_room_code = generate_room_code()

        # Level
        st.markdown('<div class="hdr">🎯 Niveau</div>', unsafe_allow_html=True)
        if "rc_level" not in st.session_state:
            st.session_state.rc_level = "🌱 Débutant"
        lc = st.columns(4)
        for i, (lname, lcfg) in enumerate(LEVELS.items()):
            with lc[i]:
                sel = st.session_state.rc_level == lname
                bdr = f"2px solid {lcfg['color']}" if sel else f"1px solid {lcfg['color']}55"
                bg  = "rgba(255,255,255,.05)" if sel else "transparent"
                st.markdown(
                    f'<div style="border:{bdr};background:{bg};border-radius:10px;padding:.5rem;'
                    f'text-align:center;color:{lcfg["color"]};font-family:Orbitron;font-size:.68rem;'
                    f'font-weight:700">{lname}<br>'
                    f'<span style="opacity:.6;font-size:.58rem">⏱{lcfg["time"]}s · {lcfg["qs"]}Q</span></div>',
                    unsafe_allow_html=True
                )
                if st.button("", key=f"rcl_{lname}", help=lname):
                    st.session_state.rc_level = lname
                    st.rerun()

        # Mode
        st.markdown('<div class="hdr">🎮 Catégorie</div>', unsafe_allow_html=True)
        mc = st.columns(2)
        for mi, (mname, mcfg) in enumerate(MODES.items()):
            with mc[mi % 2]:
                c1, c2 = st.columns([3, 1])
                with c1:
                    n = csv_row_count(mname)
                    st.markdown(
                        f'<div style="color:{mcfg["color"]};font-weight:700;font-size:.9rem">'
                        f'{mcfg["icon"]} {mname.split(" ",1)[1]}</div>'
                        f'<div style="color:#666;font-size:.7rem">{n} entrées</div>',
                        unsafe_allow_html=True
                    )
                with c2:
                    if st.button("▶", key=f"rc_{mname}", use_container_width=True):
                        code  = st.session_state.new_room_code
                        level = st.session_state.rc_level
                        lvl   = LEVELS[level]
                        qs    = build_questions(mname, lvl["key"], lvl["qs"])
                        if not qs:
                            st.error("CSV vide ou introuvable.")
                        else:
                            room_create(code, st.session_state.player_name, mname, level)
                            room_start(code, qs)
                            st.session_state.room_code = code
                            st.session_state.screen    = "room_lobby"
                            # set qtime for host's first question
                            data = room_load(code)
                            data[f"qtime_{st.session_state.player_name}_0"] = time.time()
                            _room_save(code, data)
                            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("← Retour", use_container_width=True):
            st.session_state.screen = "home"
            st.rerun()


# ══════════════════════════════════════════════════════════════
#  SCREEN: JOIN ROOM
# ══════════════════════════════════════════════════════════════
def screen_room_join():
    st.markdown('<div class="main-title" style="font-size:1.8rem">🔗 Rejoindre une salle</div>', unsafe_allow_html=True)

    cl, cc, cr = st.columns([1, 2, 1])
    with cc:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        code = st.text_input("Code de la salle", value=st.session_state.room_code,
                             placeholder="Ex: A1B2C3", key="join_code_input")
        code = code.strip().upper()

        if st.button("✅ Rejoindre", use_container_width=True):
            if not code:
                st.warning("Entrez un code de salle.")
            else:
                data = room_join(code, st.session_state.player_name)
                if data is None:
                    st.error("❌ Salle introuvable ou expirée.")
                else:
                    st.session_state.room_code = code
                    # set qtime for this player's first question
                    data[f"qtime_{st.session_state.player_name}_0"] = time.time()
                    _room_save(code, data)
                    st.session_state.screen = "room_lobby"
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("← Retour", use_container_width=True):
            st.session_state.screen = "home"
            st.rerun()


# ══════════════════════════════════════════════════════════════
#  SCREEN: ROOM LOBBY / QUIZ  (shared for all players)
# ══════════════════════════════════════════════════════════════
def screen_room():
    code  = st.session_state.room_code
    pname = st.session_state.player_name
    data  = room_load(code)

    if data is None:
        st.error("❌ Salle introuvable ou expirée.")
        if st.button("🏠 Accueil"):
            st.session_state.screen = "home"
            st.rerun()
        return

    pl       = data["players"].get(pname, {"score": 0, "q_index": 0, "done": False, "wrongs": []})
    qi       = pl.get("q_index", 0)
    qs       = data.get("questions", [])
    total    = len(qs)
    level    = data.get("level", "🌱 Débutant")
    lvl      = LEVELS.get(level, LEVELS["🌱 Débutant"])
    mode     = data.get("mode", "")
    mcfg     = MODES.get(mode, {})
    all_done = all(p.get("done", False) for p in data["players"].values())

    # ── Shareable URL ──
    try:
        base_url = st.get_option("browser.serverAddress") or ""
    except Exception:
        base_url = ""
    # Build share link note
    share_note = f"?room={code}"

    # ── Sidebar ──
    with st.sidebar:
        st.markdown(f'<div class="room-badge"><div class="room-label">Code salle</div>'
                    f'<div class="room-code">{code}</div>'
                    f'<div class="room-label">Partagez ce code !</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div style="color:#ffaa00;font-size:.75rem;text-align:center;margin:.4rem 0">'
                    f'🔗 URL: {share_note}</div>', unsafe_allow_html=True)
        st.markdown('<div class="hdr">👥 Joueurs</div>', unsafe_allow_html=True)
        for pn, pp in sorted(data["players"].items(), key=lambda x: -x[1].get("score",0)):
            done_icon = "✅ " if pp.get("done") else f"Q{pp.get('q_index',0)+1}/{total} "
            is_me = pn == pname
            st.markdown(
                f'<div class="p-row" style="{"border-color:#00ff88" if is_me else ""}">'
                f'<div style="color:#00ff88 if is_me else #aaa">{"▶ " if is_me else ""}{pn}</div>'
                f'<div style="flex:1"></div>'
                f'<div style="color:#aaa;font-size:.72rem">{done_icon}</div>'
                f'<div class="p-score">{pp.get("score",0)}</div>'
                f'</div>', unsafe_allow_html=True
            )
        st.markdown("---")
        if st.button("🏠 Accueil"):
            st.session_state.screen = "home"
            st.rerun()

    # ── Finished? ──
    if pl.get("done") or qi >= total:
        if all_done:
            _show_room_result(data, pname, lvl, mode, level)
            return
        # waiting for others
        st.markdown('<div class="main-title" style="font-size:1.6rem">⏳ En attente des autres joueurs…</div>', unsafe_allow_html=True)
        still_playing = [n for n,p in data["players"].items() if not p.get("done")]
        st.markdown(
            f'<div style="text-align:center;color:#aaa;margin-top:1rem">'
            f'Joueurs restants : {", ".join(still_playing)}</div>', unsafe_allow_html=True
        )
        time.sleep(2)
        st.rerun()
        return

    q  = qs[qi]
    tl = time_left_room(data)

    # init qtime if missing
    qtime_key = f"qtime_{pname}_{qi}"
    if qtime_key not in data:
        data[qtime_key] = time.time()
        _room_save(code, data)
        tl = lvl["time"]

    # check timeout
    if tl <= 0:
        wrong_entry = {"question":q["question"],"votre_reponse":"⌛ Temps","bonne_reponse":q["correct"]}
        room_answer(code, pname, False, 0, wrong_entry)
        # set next question timer
        ndata = room_load(code)
        if ndata:
            ndata[f"qtime_{pname}_{qi+1}"] = time.time()
            _room_save(code, ndata)
        st.rerun()
        return

    # header
    hc, tc = st.columns([3, 1])
    with hc:
        icon = mcfg.get("icon","🎮")
        mname_short = mode.split(" ",1)[1] if " " in mode else mode
        st.markdown(f'<div class="main-title" style="font-size:1.3rem;text-align:left">{icon} {mname_short}</div>', unsafe_allow_html=True)
    with tc:
        st.markdown(timer_html(tl, lvl["time"]), unsafe_allow_html=True)

    st.progress(qi / total if total else 0)
    st.markdown(f'<div style="text-align:center;color:#00d4ff55;font-size:.72rem;letter-spacing:2px">QUESTION {qi+1} / {total}</div>', unsafe_allow_html=True)

    # question
    st.markdown('<div class="q-card">', unsafe_allow_html=True)
    prompt = mcfg.get("prompt","")
    if prompt:
        st.markdown(f'<div class="q-prompt">{prompt}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="q-term">{q["question"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # choices
    c1, c2 = st.columns(2)
    for idx, ch in enumerate(q["choices"]):
        with (c1 if idx % 2 == 0 else c2):
            if st.button(f"{'ABCD'[idx]}  {ch}", key=f"ra_{qi}_{idx}_{pname}", use_container_width=True):
                ok = (ch == q["correct"])
                wrong_entry = None if ok else {"question":q["question"],"votre_reponse":ch,"bonne_reponse":q["correct"]}
                room_answer(code, pname, ok, lvl["mult"], wrong_entry)
                ndata = room_load(code)
                if ndata:
                    ndata[f"qtime_{pname}_{qi+1}"] = time.time()
                    _room_save(code, ndata)
                st.rerun()

    # auto countdown
    if tl > 0:
        time.sleep(1)
        st.rerun()


def _show_room_result(data, pname, lvl, mode, level):
    players_sorted = sorted(data["players"].items(), key=lambda x: -x[1].get("score",0))
    total = len(data.get("questions",[]))
    medals = ["🥇","🥈","🥉","4️⃣"]

    cl, cc, cr = st.columns([1, 3, 1])
    with cc:
        st.markdown('<div class="final">', unsafe_allow_html=True)
        st.markdown('<h1>🏆 CLASSEMENT FINAL</h1>', unsafe_allow_html=True)
        st.markdown(f'<div style="color:#666;font-size:.8rem;margin-bottom:1.2rem">{mode} · {level}</div>', unsafe_allow_html=True)

        for rank,(pn,pp) in enumerate(players_sorted):
            sc  = pp.get("score",0)
            pct = int(sc/(total*lvl["mult"])*100) if total else 0
            bdg, bc = badge(pct)
            is_me   = pn == pname
            st.markdown(
                f'<div style="display:flex;align-items:center;gap:.9rem;padding:.75rem 1.1rem;'
                f'background:rgba(0,0,0,.3);border:1px solid {"#00ff88" if is_me else "#333"};'
                f'border-radius:12px;margin:.35rem 0">'
                f'<div style="font-size:1.6rem">{medals[min(rank,3)]}</div>'
                f'<div style="flex:1;color:{"#00ff88" if is_me else "#fff"};font-weight:700">{pn}</div>'
                f'<div style="color:#666;font-size:.75rem">{pct}%</div>'
                f'<div style="color:#ffaa00;font-family:Orbitron;font-size:1.1rem;font-weight:900">{sc} pts</div>'
                f'</div>', unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

        # my wrongs
        my_wrongs = data["players"].get(pname,{}).get("wrongs",[])
        if my_wrongs:
            st.markdown('<div class="hdr">📖 Votre révision</div>', unsafe_allow_html=True)
            for wa in my_wrongs[:12]:
                st.markdown(f"""
                <div style="background:rgba(255,68,68,.04);border:1px solid rgba(255,68,68,.16);
                  border-radius:8px;padding:.6rem .85rem;margin:.22rem 0">
                  <div style="color:#00d4ff;font-weight:700;font-size:.85rem">{wa['question']}</div>
                  <div style="color:#ff8888;font-size:.75rem">Vous : {wa['votre_reponse']}</div>
                  <div style="color:#00ff88;font-size:.75rem">✅ {wa['bonne_reponse']}</div>
                </div>""", unsafe_allow_html=True)

        if st.button("🏠 Retour au menu", use_container_width=True):
            st.session_state.screen = "home"
            st.rerun()


# ══════════════════════════════════════════════════════════════
#  ROUTER
# ══════════════════════════════════════════════════════════════
s = st.session_state.screen
if   s == "home":         screen_home()
elif s == "solo":         screen_solo()
elif s == "solo_quiz":    screen_solo_quiz()
elif s == "solo_result":  screen_solo_result()
elif s == "room_create":  screen_room_create()
elif s == "room_join":    screen_room_join()
elif s in ("room_lobby","room_quiz","room_result"): screen_room()
else:
    st.session_state.screen = "home"
    st.rerun()
