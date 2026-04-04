import streamlit as st
import pandas as pd
import random
import time
import os
import json
import hashlib
from datetime import datetime

# ─── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="⚡ Quiz Master Pro v2",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Rajdhani', sans-serif; }
.stApp {
  background: linear-gradient(135deg, #050510 0%, #0a0a1f 40%, #050510 100%);
  min-height: 100vh;
}
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #0a0a1f 0%, #050510 100%);
  border-right: 1px solid #00d4ff22;
}

/* Title */
.main-title {
  font-family: 'Orbitron', monospace;
  font-size: 2.6rem; font-weight: 900;
  text-align: center;
  background: linear-gradient(90deg, #00d4ff, #ff00ff, #00ff88, #ffaa00, #00d4ff);
  background-size: 400% 400%;
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
  animation: gshift 4s ease infinite;
  margin-bottom: 0.2rem;
}
@keyframes gshift { 0%{background-position:0% 50%} 50%{background-position:100% 50%} 100%{background-position:0% 50%} }

.subtitle {
  text-align: center; color: #00d4ff77;
  font-size: 0.85rem; letter-spacing: 4px; text-transform: uppercase; margin-bottom: 1.5rem;
}

/* Cards */
.quiz-card {
  background: linear-gradient(135deg, rgba(0,212,255,0.04), rgba(255,0,255,0.04));
  border: 1px solid rgba(0,212,255,0.25);
  border-radius: 16px; padding: 1.5rem; margin: 0.7rem 0;
  backdrop-filter: blur(10px);
  box-shadow: 0 0 20px rgba(0,212,255,0.07), inset 0 0 20px rgba(0,0,0,0.3);
}
.question-card {
  background: linear-gradient(135deg, rgba(0,212,255,0.06), rgba(0,0,0,0.5));
  border: 1px solid rgba(0,212,255,0.5);
  border-radius: 14px; padding: 1.8rem; text-align: center; margin: 1rem 0;
  box-shadow: 0 0 30px rgba(0,212,255,0.15);
}
.question-text {
  font-family: 'Orbitron', monospace; font-size: 1.2rem;
  color: #e0f8ff; line-height: 1.6;
  text-shadow: 0 0 15px rgba(0,212,255,0.4);
}
.term-highlight {
  font-family: 'Orbitron', monospace; font-size: 1.6rem; font-weight: 900;
  color: #00ff88; margin: 0.8rem 0;
  text-shadow: 0 0 25px rgba(0,255,136,0.6);
  letter-spacing: 2px;
}

/* Timer */
.timer-danger { animation: blink 0.5s infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }
.timer-box {
  text-align: center; padding: 0.6rem 1.2rem;
  border-radius: 50px; display: inline-block;
  font-family: 'Orbitron', monospace; font-size: 1.4rem; font-weight: 900;
}
.timer-green { background: rgba(0,255,136,0.1); border: 2px solid #00ff88; color: #00ff88;
  box-shadow: 0 0 20px rgba(0,255,136,0.3); }
.timer-yellow { background: rgba(255,170,0,0.1); border: 2px solid #ffaa00; color: #ffaa00;
  box-shadow: 0 0 20px rgba(255,170,0,0.3); }
.timer-red { background: rgba(255,50,50,0.1); border: 2px solid #ff4444; color: #ff4444;
  box-shadow: 0 0 20px rgba(255,68,68,0.4); animation: blink 0.5s infinite; }

/* Level badges */
.badge-debutant   { color:#00d4ff; border:1px solid #00d4ff; background:rgba(0,212,255,0.1); }
.badge-potentiel  { color:#00ff88; border:1px solid #00ff88; background:rgba(0,255,136,0.1); }
.badge-legende    { color:#ffaa00; border:1px solid #ffaa00; background:rgba(255,170,0,0.1); }
.badge-superstar  { color:#ff00ff; border:1px solid #ff00ff; background:rgba(255,0,255,0.1); }
.badge-base { padding:0.3rem 1rem; border-radius:50px; font-family:'Orbitron',monospace;
  font-size:0.75rem; font-weight:700; letter-spacing:2px; display:inline-block; margin:0.2rem; }

/* Notifications */
.notif-correct {
  background: linear-gradient(135deg, rgba(0,255,136,0.12), rgba(0,200,100,0.06));
  border: 2px solid #00ff88; border-radius: 14px; padding: 1.5rem; text-align: center;
  animation: popIn 0.4s cubic-bezier(0.34,1.56,0.64,1);
  box-shadow: 0 0 50px rgba(0,255,136,0.35), 0 0 100px rgba(0,255,136,0.1);
  margin: 1rem 0;
}
.notif-wrong {
  background: linear-gradient(135deg, rgba(255,50,50,0.12), rgba(200,0,0,0.06));
  border: 2px solid #ff4444; border-radius: 14px; padding: 1.5rem; text-align: center;
  animation: shake 0.5s ease;
  box-shadow: 0 0 50px rgba(255,68,68,0.35), 0 0 100px rgba(255,68,68,0.1);
  margin: 1rem 0;
}
.notif-timeout {
  background: linear-gradient(135deg, rgba(255,170,0,0.12), rgba(200,100,0,0.06));
  border: 2px solid #ffaa00; border-radius: 14px; padding: 1.5rem; text-align: center;
  animation: popIn 0.4s ease;
  box-shadow: 0 0 50px rgba(255,170,0,0.35);
  margin: 1rem 0;
}
@keyframes popIn {
  0%{transform:scale(0.7);opacity:0} 80%{transform:scale(1.05)} 100%{transform:scale(1);opacity:1}
}
@keyframes shake {
  0%,100%{transform:translateX(0)} 20%{transform:translateX(-10px)} 40%{transform:translateX(10px)}
  60%{transform:translateX(-8px)} 80%{transform:translateX(8px)}
}
.notif-correct h2{color:#00ff88;font-family:'Orbitron',monospace;font-size:1.5rem;margin:0;text-shadow:0 0 20px #00ff88;}
.notif-wrong   h2{color:#ff4444;font-family:'Orbitron',monospace;font-size:1.5rem;margin:0;text-shadow:0 0 20px #ff4444;}
.notif-timeout h2{color:#ffaa00;font-family:'Orbitron',monospace;font-size:1.5rem;margin:0;text-shadow:0 0 20px #ffaa00;}
.notif-correct p,.notif-wrong p,.notif-timeout p{color:#ccc;font-size:0.95rem;margin-top:0.5rem;}

/* Score */
.score-box {
  background: linear-gradient(135deg, rgba(255,170,0,0.1), rgba(255,0,255,0.05));
  border: 1px solid rgba(255,170,0,0.4); border-radius: 12px;
  padding: 1rem; text-align: center; margin-bottom: 1rem;
}
.score-box h3{color:#ffaa00;font-family:'Orbitron',monospace;font-size:0.8rem;margin:0;}
.score-box .big{color:#fff;font-family:'Orbitron',monospace;font-size:2rem;font-weight:900;}

/* Multiplayer */
.player-row {
  display:flex; align-items:center; gap:0.8rem;
  background:rgba(0,212,255,0.05); border:1px solid rgba(0,212,255,0.2);
  border-radius:10px; padding:0.7rem 1rem; margin:0.4rem 0;
}
.player-color { width:14px;height:14px;border-radius:50%;flex-shrink:0; }
.player-name { color:#fff;font-weight:600;flex:1; }
.player-score { color:#ffaa00;font-family:'Orbitron',monospace;font-weight:700; }
.active-player { border-color:#00ff88 !important; box-shadow:0 0 15px rgba(0,255,136,0.2); }

/* Final */
.final-card {
  background: linear-gradient(135deg, rgba(0,212,255,0.07), rgba(255,0,255,0.05));
  border: 2px solid rgba(0,212,255,0.4);
  border-radius: 20px; padding: 2.5rem; text-align: center;
  box-shadow: 0 0 60px rgba(0,212,255,0.15);
  animation: popIn 0.8s ease;
}
.final-card h1{font-family:'Orbitron',monospace;color:#00ff88;font-size:2rem;text-shadow:0 0 30px #00ff88;}
.final-score{font-family:'Orbitron',monospace;font-size:3.5rem;font-weight:900;color:#ffaa00;text-shadow:0 0 40px #ffaa00;}
.podium-1{color:#ffd700;font-size:1.3rem;font-weight:700;}
.podium-2{color:#c0c0c0;font-size:1.1rem;font-weight:700;}
.podium-3{color:#cd7f32;font-size:1rem;font-weight:700;}

/* Buttons */
.stButton>button {
  width:100%; padding:0.85rem 1rem;
  font-family:'Rajdhani',sans-serif; font-size:1rem; font-weight:600;
  border-radius:10px; border:1px solid rgba(0,212,255,0.35);
  background:linear-gradient(135deg,rgba(0,212,255,0.07),rgba(0,0,0,0.5));
  color:#e0f0ff; cursor:pointer; transition:all 0.2s ease; letter-spacing:0.5px;
}
.stButton>button:hover {
  background:linear-gradient(135deg,rgba(0,212,255,0.18),rgba(255,0,255,0.08));
  border-color:#00d4ff; color:#fff;
  box-shadow:0 0 20px rgba(0,212,255,0.35),0 0 40px rgba(0,212,255,0.1);
  transform:translateY(-2px);
}

.section-hdr {
  color:#00d4ff; font-size:0.75rem; letter-spacing:3px; text-transform:uppercase;
  border-bottom:1px solid rgba(0,212,255,0.25); padding-bottom:0.3rem; margin:1.2rem 0 0.8rem;
}
.player-tag {
  text-align:center; font-family:'Orbitron',monospace; color:#ffaa00;
  font-size:0.8rem; letter-spacing:2px; padding:0.5rem;
  border-bottom:1px solid rgba(255,170,0,0.25); margin-bottom:0.8rem;
}
.progress-lbl{color:#00d4ff;font-size:0.78rem;letter-spacing:2px;text-transform:uppercase;margin-bottom:0.25rem;}

/* Input */
.stTextInput>div>div>input {
  background:rgba(0,212,255,0.04); border:1px solid rgba(0,212,255,0.3);
  color:white; border-radius:8px;
}
.stSelectbox>div>div{background:rgba(0,212,255,0.04);border:1px solid rgba(0,212,255,0.3);border-radius:8px;}
#MainMenu,footer,header{visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ─── CONSTANTS ────────────────────────────────────────────────────────────────
BASE = os.path.dirname(__file__)
DATA = os.path.join(BASE, "data")

PLAYER_COLORS = ["#00d4ff", "#ff00ff", "#00ff88", "#ffaa00"]
PLAYER_EMOJIS = ["🔵", "🟣", "🟢", "🟡"]

LEVELS = {
    "🌱 Débutant":   {"key":"debutant",  "time":30, "qs":10, "color":"#00d4ff", "multiplier":1},
    "⚡ Potentiel":  {"key":"potentiel", "time":20, "qs":15, "color":"#00ff88", "multiplier":2},
    "🔥 Légende":    {"key":"legende",   "time":15, "qs":20, "color":"#ffaa00", "multiplier":3},
    "👑 Superstar":  {"key":"superstar", "time":10, "qs":25, "color":"#ff00ff", "multiplier":5},
}

MODES = {
    "🔐 Sécurité Financière": {
        "file":"securite_financiere.csv","type":"vocab",
        "col_q":"Terme","col_a":"Definition",
        "prompt":"Quelle est la définition de :","color":"#00d4ff","icon":"🏦",
        "desc":"Vocabulaire AML/KYC/Compliance professionnel"
    },
    "🇫🇷 Français":{"file":"apprentissage_francais.csv","type":"vocab",
        "col_q":"Mot_Expression","col_a":"Definition_Synonyme",
        "prompt":"Synonyme ou définition de :","color":"#ff00ff","icon":"📚",
        "desc":"Vocabulaire et expressions françaises"
    },
    "🇬🇧 Anglais":{"file":"anglais.csv","type":"vocab",
        "col_q":"Mot_Expression","col_a":"Definition_EN",
        "prompt":"What is the definition of:","color":"#00ffff","icon":"🌐",
        "desc":"English vocabulary and idioms"
    },
    "🇪🇸 Espagnol":{"file":"espagnol.csv","type":"vocab",
        "col_q":"Mot_Expression","col_a":"Definition_ES",
        "prompt":"¿Cuál es la definición de:","color":"#ff6600","icon":"🌮",
        "desc":"Vocabulario y expresiones en español"
    },
    "🇭🇹 Créole Haïtien":{"file":"creole_haitien.csv","type":"vocab",
        "col_q":"Mot_Expression","col_a":"Definition_Kreyol",
        "prompt":"Ki definisyon oswa sinonim:","color":"#ff0044","icon":"🌴",
        "desc":"Mo ak ekspresyon an kreyòl ayisyen"
    },
    "🏛️ Monuments":{"file":"monuments_monde.csv","type":"vocab",
        "col_q":"Monument","col_a":"Pays",
        "prompt":"Dans quel pays se trouve :","color":"#ffaa00","icon":"🌍",
        "desc":"Monuments historiques du monde entier"
    },
    "🎵 Musique":{"file":"musique_monde.csv","type":"music",
        "col_q":"Artiste","col_a":"Chanson",
        "prompt":"Quelle est la chanson de :","color":"#ff00aa","icon":"🎶",
        "desc":"Artistes et chansons haïtiens & mondiaux"
    },
    "🔢 Mathématiques":{"file":"mathematiques.csv","type":"math",
        "col_q":"Question","col_a":"Reponse",
        "prompt":"Résolvez :","color":"#00ff88","icon":"🧮",
        "desc":"Algèbre et calcul — tous niveaux"
    },
    "🏺 Histoire":{"file":"histoire.csv","type":"mcq",
        "col_q":"Question","col_a":"Reponse_Correcte",
        "prompt":"","color":"#ff8800","icon":"📜",
        "desc":"France, Haïti & Histoire mondiale"
    },
    "🌐 Culture Générale":{"file":"culture_generale.csv","type":"mcq",
        "col_q":"Question","col_a":"Reponse_Correcte",
        "prompt":"","color":"#aa00ff","icon":"🧠",
        "desc":"Sciences, Géo, Art, Sports & plus"
    },
}

# ─── DATA LOADING ──────────────────────────────────────────────────────────────
@st.cache_data
def load_csv(filename):
    path = os.path.join(DATA, filename)
    if not os.path.exists(path):
        return pd.DataFrame()
    return pd.read_csv(path)

def get_df(mode_name):
    return load_csv(MODES[mode_name]["file"])

# ─── QUESTION BUILDING ─────────────────────────────────────────────────────────
def build_questions(mode_name, level_key, n):
    cfg = MODES[mode_name]
    df  = get_df(mode_name).dropna()
    
    # Filter by level for math/history/culture
    if cfg["type"] in ("math","mcq") and "Difficulte" in df.columns and level_key != "debutant":
        # Include current and lower levels
        order = ["debutant","potentiel","legende","superstar"]
        idx   = order.index(level_key)
        allowed = order[:idx+1]
        df = df[df["Difficulte"].isin(allowed)]
    elif cfg["type"] in ("math","mcq") and "Difficulte" in df.columns:
        df = df[df["Difficulte"] == "debutant"]
    
    if len(df) == 0:
        df = get_df(mode_name).dropna()
    
    df = df.sample(frac=1).reset_index(drop=True)
    n  = min(n, len(df))
    qs = []
    
    for i in range(n):
        row   = df.iloc[i]
        right = str(row[cfg["col_a"]])
        
        # For MCQ types, use provided choices
        if cfg["type"] == "mcq" and "Choix_2" in df.columns:
            choices = [right]
            for cx in ["Choix_2","Choix_3","Choix_4"]:
                if cx in df.columns and pd.notna(row.get(cx)):
                    choices.append(str(row[cx]))
            # Fill with random from df if not enough
            while len(choices) < 4:
                sample = df[df[cfg["col_a"]] != right][cfg["col_a"]].dropna()
                if len(sample) > 0:
                    choices.append(str(random.choice(sample.values)))
                else:
                    break
            choices = list(dict.fromkeys(choices))[:4]
            random.shuffle(choices)
        else:
            pool  = df[df[cfg["col_a"]] != right][cfg["col_a"]].dropna()
            wrongs = pool.sample(min(3, len(pool))).tolist()
            choices = [right] + [str(w) for w in wrongs]
            random.shuffle(choices)
        
        qs.append({
            "question": str(row[cfg["col_q"]]),
            "correct":  right,
            "choices":  choices,
            "prompt":   cfg["prompt"],
        })
    return qs

# ─── SESSION STATE ─────────────────────────────────────────────────────────────
def init_state():
    defs = {
        "screen":"home",
        "players":[],       # list of {"name":str,"score":int,"wrongs":[]}
        "n_players":1,
        "cur_player":0,     # index in players list
        "game_mode":None,
        "level_name":None,
        "questions":[],
        "q_index":0,
        "answer_given":False,
        "last_correct":None,
        "timed_out":False,
        "q_start_time":None,
    }
    for k,v in defs.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ─── HELPERS ──────────────────────────────────────────────────────────────────
def time_left():
    if st.session_state.q_start_time is None:
        return 99
    level = LEVELS[st.session_state.level_name]
    elapsed = time.time() - st.session_state.q_start_time
    return max(0, level["time"] - int(elapsed))

def get_badge(pct):
    if pct >= 90: return "🏆 LÉGENDAIRE", "#00ff88"
    if pct >= 70: return "⭐ EXPERT",      "#ffaa00"
    if pct >= 50: return "👍 BIEN",        "#00d4ff"
    return "📚 À REVOIR", "#ff4444"

def cur_player():
    idx = st.session_state.cur_player
    return st.session_state.players[idx] if idx < len(st.session_state.players) else None

def reset_quiz():
    for p in st.session_state.players:
        p["score"] = 0
        p["wrongs"] = []
    st.session_state.q_index      = 0
    st.session_state.cur_player   = 0
    st.session_state.answer_given = False
    st.session_state.last_correct = None
    st.session_state.timed_out    = False
    st.session_state.q_start_time = None

# ─── SCREEN: HOME ─────────────────────────────────────────────────────────────
def screen_home():
    st.markdown('<div class="main-title">⚡ QUIZ MASTER PRO</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">10 Univers · 4 Niveaux · Compétition Multijoueur</div>', unsafe_allow_html=True)

    col_l, col_c, col_r = st.columns([0.5, 3, 0.5])
    with col_c:
        # ── Multiplayer setup ──
        with st.container():
            st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-hdr">👥 Participants</div>', unsafe_allow_html=True)
            
            n_players = st.select_slider(
                "Nombre de joueurs",
                options=[1,2,3,4],
                value=st.session_state.n_players,
                label_visibility="collapsed"
            )
            st.session_state.n_players = n_players
            
            cols_p = st.columns(n_players)
            players = []
            for i in range(n_players):
                with cols_p[i]:
                    st.markdown(f'<div style="color:{PLAYER_COLORS[i]};font-weight:700;font-size:0.85rem">'
                                f'{PLAYER_EMOJIS[i]} Joueur {i+1}</div>', unsafe_allow_html=True)
                    existing = st.session_state.players[i]["name"] if i < len(st.session_state.players) else ""
                    name = st.text_input(f"", value=existing,
                                         placeholder=f"Joueur {i+1}",
                                         key=f"pname_{i}",
                                         label_visibility="collapsed")
                    players.append({"name": name or f"Joueur {i+1}", "score": 0, "wrongs": []})
            
            # ── Level ──
            st.markdown('<div class="section-hdr">🎯 Niveau de difficulté</div>', unsafe_allow_html=True)
            level_cols = st.columns(4)
            selected_level = st.session_state.level_name or "🌱 Débutant"
            for i, (lname, lcfg) in enumerate(LEVELS.items()):
                with level_cols[i]:
                    badge_cls = f"badge-{lcfg['key']}"
                    is_sel = (lname == selected_level)
                    border = "2px solid" if is_sel else "1px solid"
                    bg = "rgba(255,255,255,0.05)" if is_sel else "transparent"
                    st.markdown(
                        f'<div class="badge-base {badge_cls}" style="border:{border};background:{bg};'
                        f'text-align:center;padding:0.5rem;width:100%;border-radius:10px;cursor:pointer">'
                        f'{lname}<br><span style="font-size:0.65rem;opacity:0.7">'
                        f'⏱{lcfg["time"]}s · {lcfg["qs"]}Q</span></div>',
                        unsafe_allow_html=True
                    )
                    if st.button(f"", key=f"lvl_{lname}", help=lname):
                        st.session_state.level_name = lname
                        st.rerun()
            
            if not selected_level:
                st.session_state.level_name = "🌱 Débutant"
            
            st.markdown('</div>', unsafe_allow_html=True)

        # ── Game modes ──
        st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-hdr">🎮 Choisissez votre univers</div>', unsafe_allow_html=True)

        mode_cols = st.columns(2)
        for mi, (mname, mcfg) in enumerate(MODES.items()):
            with mode_cols[mi % 2]:
                c1, c2 = st.columns([3,1])
                with c1:
                    st.markdown(
                        f'<div style="color:{mcfg["color"]};font-weight:700;font-size:1rem">'
                        f'{mcfg["icon"]} {mname.split(" ",1)[1]}</div>'
                        f'<div style="color:#888;font-size:0.78rem;margin-bottom:0.2rem">{mcfg["desc"]}</div>',
                        unsafe_allow_html=True
                    )
                with c2:
                    if st.button("JOUER", key=f"go_{mname}"):
                        lvl_cfg = LEVELS[st.session_state.level_name or "🌱 Débutant"]
                        st.session_state.players = players
                        st.session_state.game_mode = mname
                        reset_quiz()
                        st.session_state.questions = build_questions(
                            mname, lvl_cfg["key"], lvl_cfg["qs"]
                        )
                        st.session_state.screen = "quiz"
                        st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Stats bar
    st.markdown("<br>", unsafe_allow_html=True)
    stat_cols = st.columns(5)
    stats = [
        ("🔐", "Finance", len(get_df("🔐 Sécurité Financière")), "#00d4ff"),
        ("🇫🇷", "Français", len(get_df("🇫🇷 Français")), "#ff00ff"),
        ("🌍", "Monuments", len(get_df("🏛️ Monuments")), "#ffaa00"),
        ("🎵", "Musique", len(get_df("🎵 Musique")), "#ff00aa"),
        ("🧠", "Culture", len(get_df("🌐 Culture Générale")), "#aa00ff"),
    ]
    for i,(icon,label,count,color) in enumerate(stats):
        with stat_cols[i]:
            st.markdown(f'<div class="quiz-card" style="text-align:center;padding:1rem">'
                        f'<div style="font-size:1.5rem">{icon}</div>'
                        f'<div style="color:{color};font-family:Orbitron;font-size:0.65rem;letter-spacing:2px">{label.upper()}</div>'
                        f'<div style="color:#fff;font-size:1.2rem;font-weight:700">{count}</div>'
                        f'</div>', unsafe_allow_html=True)

# ─── SCREEN: QUIZ ─────────────────────────────────────────────────────────────
def screen_quiz():
    qs     = st.session_state.questions
    qi     = st.session_state.q_index
    total  = len(qs)
    lvl    = LEVELS[st.session_state.level_name or "🌱 Débutant"]
    mode   = st.session_state.game_mode
    mcfg   = MODES[mode]
    n_pl   = len(st.session_state.players)

    if qi >= total:
        st.session_state.screen = "result"
        st.rerun()
        return

    q = qs[qi]
    cp = st.session_state.players[st.session_state.cur_player]

    # Init timer for this question
    if st.session_state.q_start_time is None and not st.session_state.answer_given:
        st.session_state.q_start_time = time.time()

    # Check timeout
    tl = time_left()
    if tl <= 0 and not st.session_state.answer_given:
        st.session_state.answer_given = True
        st.session_state.timed_out    = True
        st.session_state.last_correct = False
        cp["wrongs"].append({
            "question": q["question"],
            "votre_reponse": "⌛ Temps écoulé",
            "bonne_reponse": q["correct"]
        })

    # ─── Sidebar ───
    with st.sidebar:
        if n_pl > 1:
            st.markdown('<div class="section-hdr" style="margin-top:0">👥 Scores</div>', unsafe_allow_html=True)
            for pi, pl in enumerate(st.session_state.players):
                active = (pi == st.session_state.cur_player)
                aclass = " active-player" if active else ""
                st.markdown(
                    f'<div class="player-row{aclass}">'
                    f'<div class="player-color" style="background:{PLAYER_COLORS[pi]}"></div>'
                    f'<div class="player-name">{"▶ " if active else ""}{pl["name"]}</div>'
                    f'<div class="player-score">{pl["score"]}</div>'
                    f'</div>', unsafe_allow_html=True
                )
        else:
            st.markdown(f'<div class="player-tag">👤 {cp["name"].upper()}</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="score-box"><h3>⚡ SCORE</h3>'
                f'<div class="big">{cp["score"]}/{qi}</div></div>',
                unsafe_allow_html=True
            )

        lc = lvl["color"]
        st.markdown(
            f'<div style="margin-top:0.8rem;padding:0.8rem;background:rgba(0,0,0,0.3);'
            f'border:1px solid {lc}33;border-radius:10px;text-align:center">'
            f'<div style="color:{lc};font-family:Orbitron;font-size:0.75rem;letter-spacing:2px">'
            f'{st.session_state.level_name}</div>'
            f'<div style="color:#aaa;font-size:0.8rem;margin-top:0.3rem">'
            f'Q {qi+1}/{total} · ×{lvl["multiplier"]} pts</div>'
            f'</div>', unsafe_allow_html=True
        )

        st.markdown('<div class="progress-lbl" style="margin-top:0.8rem">Progression</div>', unsafe_allow_html=True)
        st.progress(qi / total if total else 0)

        st.markdown("---")
        if st.button("🏠 Accueil", use_container_width=True):
            st.session_state.screen = "home"
            st.rerun()

    # ─── Main content ───
    head_c, timer_c = st.columns([3,1])
    with head_c:
        st.markdown(f'<div class="main-title" style="font-size:1.5rem;text-align:left">'
                    f'{mcfg["icon"]} {mode.split(" ",1)[1]}</div>', unsafe_allow_html=True)
    with timer_c:
        if not st.session_state.answer_given:
            pct_t = tl / lvl["time"]
            tcls = "timer-green" if pct_t > 0.5 else ("timer-yellow" if pct_t > 0.25 else "timer-red")
            st.markdown(f'<div style="text-align:right">'
                        f'<div class="timer-box {tcls}">⏱ {tl}s</div></div>',
                        unsafe_allow_html=True)

    # Multiplayer turn indicator
    if n_pl > 1:
        st.markdown(
            f'<div style="text-align:center;margin:0.3rem 0;padding:0.5rem;'
            f'background:rgba({PLAYER_COLORS[st.session_state.cur_player].replace("#","")},0.1);'
            f'border-radius:8px;color:{PLAYER_COLORS[st.session_state.cur_player]};'
            f'font-family:Orbitron;font-size:0.9rem;letter-spacing:2px">'
            f'Tour de : {cp["name"].upper()}</div>',
            unsafe_allow_html=True
        )

    st.progress(qi / total if total else 0)
    st.markdown(
        f'<div style="text-align:center;color:#00d4ff66;font-size:0.75rem;'
        f'letter-spacing:2px">QUESTION {qi+1} / {total}</div>',
        unsafe_allow_html=True
    )

    # Question card
    st.markdown('<div class="question-card">', unsafe_allow_html=True)
    if q["prompt"]:
        st.markdown(f'<div class="question-text">{q["prompt"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="term-highlight">{q["question"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Notification or choices
    if st.session_state.answer_given:
        if st.session_state.timed_out:
            st.markdown(f"""
            <div class="notif-timeout">
              <h2>⌛ TEMPS ÉCOULÉ !</h2>
              <p>La réponse était : <strong style="color:#ffaa00">{q['correct']}</strong></p>
            </div>""", unsafe_allow_html=True)
        elif st.session_state.last_correct:
            pts = lvl["multiplier"]
            st.markdown(f"""
            <div class="notif-correct">
              <h2>✅ CORRECT ! +{pts} pt{'s' if pts>1 else ''}</h2>
              <p><strong style="color:#00ff88">{q['correct']}</strong></p>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="notif-wrong">
              <h2>❌ INCORRECT</h2>
              <p>Bonne réponse : <strong style="color:#ff6666">{q['correct']}</strong></p>
            </div>""", unsafe_allow_html=True)

        if st.button("➡️ Question suivante", use_container_width=True):
            st.session_state.q_index += 1
            st.session_state.answer_given  = False
            st.session_state.last_correct  = None
            st.session_state.timed_out     = False
            st.session_state.q_start_time  = None
            # Rotate players for multiplayer
            if n_pl > 1:
                st.session_state.cur_player = (st.session_state.cur_player + 1) % n_pl
            st.rerun()
    else:
        c1, c2 = st.columns(2)
        for idx, choice in enumerate(q["choices"]):
            with (c1 if idx % 2 == 0 else c2):
                label = f"{'ABCD'[idx]}  {choice}"
                if st.button(label, key=f"ch_{qi}_{idx}", use_container_width=True):
                    correct = (choice == q["correct"])
                    st.session_state.answer_given = True
                    st.session_state.last_correct = correct
                    st.session_state.timed_out    = False
                    if correct:
                        cp["score"] += lvl["multiplier"]
                    else:
                        cp["wrongs"].append({
                            "question": q["question"],
                            "votre_reponse": choice,
                            "bonne_reponse": q["correct"]
                        })
                    st.rerun()

        # Auto-rerun for timer countdown
        if not st.session_state.answer_given and tl > 0:
            time.sleep(1)
            st.rerun()

# ─── SCREEN: RESULT ───────────────────────────────────────────────────────────
def screen_result():
    players  = st.session_state.players
    total    = len(st.session_state.questions)
    mode     = st.session_state.game_mode
    lvl      = LEVELS[st.session_state.level_name or "🌱 Débutant"]
    n_pl     = len(players)

    sorted_p = sorted(players, key=lambda x: x["score"], reverse=True)

    with st.sidebar:
        if st.button("🏠 Accueil", use_container_width=True):
            st.session_state.screen = "home"
            st.rerun()
        if st.button("🔄 Rejouer", use_container_width=True):
            reset_quiz()
            st.session_state.questions = build_questions(
                mode, lvl["key"], lvl["qs"]
            )
            st.session_state.screen = "quiz"
            st.rerun()

    col_l, col_c, col_r = st.columns([0.5, 3, 0.5])
    with col_c:
        if n_pl == 1:
            p    = players[0]
            pct  = int(p["score"] / (total * lvl["multiplier"]) * 100) if total else 0
            badge, bc = get_badge(pct)
            st.markdown(f"""
            <div class="final-card">
              <h1>🎯 RÉSULTATS FINAUX</h1>
              <div style="color:#00d4ff88;font-family:Orbitron;font-size:0.8rem;letter-spacing:3px">{p['name'].upper()}</div>
              <div class="final-score">{p['score']} pts</div>
              <div style="font-size:1.2rem;margin:0.3rem">{pct}%</div>
              <div style="color:{bc};font-family:Orbitron;font-size:1.2rem;font-weight:700;
                           text-shadow:0 0 20px {bc};margin:0.8rem 0">{badge}</div>
              <div style="color:#666;font-size:0.85rem">{mode} · {st.session_state.level_name}</div>
            </div>""", unsafe_allow_html=True)
        else:
            # Multiplayer podium
            st.markdown('<div class="final-card">', unsafe_allow_html=True)
            st.markdown('<h1 style="color:#00ff88;font-family:Orbitron">🏆 CLASSEMENT FINAL</h1>', unsafe_allow_html=True)
            st.markdown(f'<div style="color:#666;font-size:0.85rem;margin-bottom:1.5rem">{mode} · {st.session_state.level_name}</div>', unsafe_allow_html=True)
            
            medals = ["🥇","🥈","🥉","4️⃣"]
            for rank, pl in enumerate(sorted_p):
                pi = players.index(pl)
                st.markdown(
                    f'<div style="display:flex;align-items:center;gap:1rem;padding:0.8rem 1.2rem;'
                    f'background:rgba(0,0,0,0.3);border:1px solid {PLAYER_COLORS[pi]}44;'
                    f'border-radius:12px;margin:0.4rem 0">'
                    f'<div style="font-size:1.8rem">{medals[rank]}</div>'
                    f'<div style="color:{PLAYER_COLORS[pi]};font-size:1rem;font-weight:700;flex:1">'
                    f'{pl["name"]}</div>'
                    f'<div style="color:#ffaa00;font-family:Orbitron;font-size:1.3rem;font-weight:900">'
                    f'{pl["score"]} pts</div>'
                    f'</div>', unsafe_allow_html=True
                )
            st.markdown('</div>', unsafe_allow_html=True)

        # Stats
        st.markdown("<br>", unsafe_allow_html=True)
        sc1,sc2,sc3 = st.columns(3)
        best = sorted_p[0]
        with sc1:
            st.markdown(f'<div class="quiz-card" style="text-align:center">'
                        f'<div style="font-size:1.5rem">🏆</div>'
                        f'<div style="color:#ffaa00;font-family:Orbitron;font-size:0.7rem">MEILLEUR</div>'
                        f'<div style="color:#fff;font-size:1rem;font-weight:700">{best["name"]}</div>'
                        f'<div style="color:#ffaa00;font-family:Orbitron">{best["score"]} pts</div>'
                        f'</div>', unsafe_allow_html=True)
        with sc2:
            st.markdown(f'<div class="quiz-card" style="text-align:center">'
                        f'<div style="font-size:1.5rem">📊</div>'
                        f'<div style="color:#00d4ff;font-family:Orbitron;font-size:0.7rem">QUESTIONS</div>'
                        f'<div style="color:#fff;font-size:1.3rem;font-weight:700">{total}</div>'
                        f'</div>', unsafe_allow_html=True)
        with sc3:
            tot_wrong = sum(len(p["wrongs"]) for p in players)
            st.markdown(f'<div class="quiz-card" style="text-align:center">'
                        f'<div style="font-size:1.5rem">❌</div>'
                        f'<div style="color:#ff4444;font-family:Orbitron;font-size:0.7rem">ERREURS</div>'
                        f'<div style="color:#fff;font-size:1.3rem;font-weight:700">{tot_wrong}</div>'
                        f'</div>', unsafe_allow_html=True)

        # Wrong answers per player
        for pl in players:
            if pl["wrongs"]:
                pi = players.index(pl)
                st.markdown(f'<div class="section-hdr">📖 Révision — {pl["name"]}</div>', unsafe_allow_html=True)
                for wa in pl["wrongs"][:10]:
                    st.markdown(f"""
                    <div style="background:rgba(255,68,68,0.04);border:1px solid rgba(255,68,68,0.2);
                      border-radius:8px;padding:0.7rem 1rem;margin:0.3rem 0">
                      <div style="color:#00d4ff;font-weight:700;font-size:0.9rem">{wa['question']}</div>
                      <div style="color:#ff8888;font-size:0.82rem">Votre réponse : {wa['votre_reponse']}</div>
                      <div style="color:#00ff88;font-size:0.82rem">✅ {wa['bonne_reponse']}</div>
                    </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        b1, b2 = st.columns(2)
        with b1:
            if st.button("🔄 Rejouer", use_container_width=True):
                reset_quiz()
                st.session_state.questions = build_questions(mode, lvl["key"], lvl["qs"])
                st.session_state.screen = "quiz"
                st.rerun()
        with b2:
            if st.button("🏠 Changer de mode", use_container_width=True):
                st.session_state.screen = "home"
                st.rerun()

# ─── ROUTER ───────────────────────────────────────────────────────────────────
if   st.session_state.screen == "home":   screen_home()
elif st.session_state.screen == "quiz":   screen_quiz()
elif st.session_state.screen == "result": screen_result()
