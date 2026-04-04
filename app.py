import streamlit as st
import pandas as pd
import random
import time
import os

# ─── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🎓 Quiz Master Pro",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CUSTOM CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&display=swap');

  /* ── Global ── */
  html, body, [class*="css"] {
    font-family: 'Rajdhani', sans-serif;
  }
  .stApp {
    background: linear-gradient(135deg, #0a0a1a 0%, #0d1b2a 40%, #0a1628 100%);
    min-height: 100vh;
  }

  /* ── Sidebar ── */
  [data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1b2a 0%, #0a0a1a 100%);
    border-right: 1px solid #00d4ff33;
  }

  /* ── Title ── */
  .main-title {
    font-family: 'Orbitron', monospace;
    font-size: 2.8rem;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(90deg, #00d4ff, #ff00ff, #00ff88, #ffaa00);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: gradient-shift 3s ease infinite;
    margin-bottom: 0.2rem;
    text-shadow: none;
  }
  @keyframes gradient-shift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
  }
  .subtitle {
    text-align: center;
    color: #00d4ff99;
    font-size: 1rem;
    font-family: 'Rajdhani', sans-serif;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 2rem;
  }

  /* ── Cards ── */
  .quiz-card {
    background: linear-gradient(135deg, rgba(0,212,255,0.05), rgba(255,0,255,0.05));
    border: 1px solid rgba(0,212,255,0.3);
    border-radius: 16px;
    padding: 2rem;
    margin: 1rem 0;
    backdrop-filter: blur(10px);
    box-shadow: 0 0 30px rgba(0,212,255,0.1), inset 0 0 30px rgba(0,0,0,0.3);
  }
  .question-text {
    font-family: 'Orbitron', monospace;
    font-size: 1.4rem;
    color: #ffffff;
    text-align: center;
    padding: 1.5rem;
    background: linear-gradient(135deg, rgba(0,212,255,0.08), rgba(0,0,0,0.4));
    border: 1px solid rgba(0,212,255,0.4);
    border-radius: 12px;
    margin-bottom: 1.5rem;
    text-shadow: 0 0 20px rgba(0,212,255,0.5);
  }
  .term-display {
    font-family: 'Orbitron', monospace;
    font-size: 1.8rem;
    font-weight: 900;
    color: #00ff88;
    text-align: center;
    margin: 1rem 0;
    text-shadow: 0 0 30px rgba(0,255,136,0.7);
    letter-spacing: 2px;
  }

  /* ── Buttons (override Streamlit) ── */
  .stButton > button {
    width: 100%;
    padding: 0.9rem 1rem;
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.05rem;
    font-weight: 600;
    border-radius: 10px;
    border: 1px solid rgba(0,212,255,0.4);
    background: linear-gradient(135deg, rgba(0,212,255,0.08), rgba(0,0,0,0.5));
    color: #e0f0ff;
    cursor: pointer;
    transition: all 0.25s ease;
    letter-spacing: 0.5px;
  }
  .stButton > button:hover {
    background: linear-gradient(135deg, rgba(0,212,255,0.2), rgba(255,0,255,0.1));
    border-color: #00d4ff;
    color: #ffffff;
    box-shadow: 0 0 20px rgba(0,212,255,0.4), 0 0 40px rgba(0,212,255,0.15);
    transform: translateY(-2px);
  }

  /* ── Notification overlays ── */
  .notif-correct {
    background: linear-gradient(135deg, rgba(0,255,136,0.15), rgba(0,200,100,0.08));
    border: 2px solid #00ff88;
    border-radius: 14px;
    padding: 1.5rem;
    text-align: center;
    animation: pulse-green 0.6s ease;
    box-shadow: 0 0 40px rgba(0,255,136,0.4), inset 0 0 20px rgba(0,255,136,0.05);
    margin: 1rem 0;
  }
  .notif-wrong {
    background: linear-gradient(135deg, rgba(255,50,50,0.15), rgba(200,0,0,0.08));
    border: 2px solid #ff4444;
    border-radius: 14px;
    padding: 1.5rem;
    text-align: center;
    animation: pulse-red 0.6s ease;
    box-shadow: 0 0 40px rgba(255,68,68,0.4), inset 0 0 20px rgba(255,68,68,0.05);
    margin: 1rem 0;
  }
  @keyframes pulse-green {
    0%   { transform: scale(0.95); opacity:0; }
    60%  { transform: scale(1.03); opacity:1; }
    100% { transform: scale(1); }
  }
  @keyframes pulse-red {
    0%   { transform: scale(0.95); opacity:0; }
    60%  { transform: scale(1.03); opacity:1; }
    100% { transform: scale(1); }
  }
  .notif-correct h2 { color: #00ff88; font-family:'Orbitron',monospace; font-size:1.6rem; margin:0; text-shadow:0 0 20px #00ff88; }
  .notif-wrong   h2 { color: #ff4444; font-family:'Orbitron',monospace; font-size:1.6rem; margin:0; text-shadow:0 0 20px #ff4444; }
  .notif-correct p, .notif-wrong p { color:#ddd; font-size:1rem; margin-top:0.5rem; }

  /* ── Score box ── */
  .score-box {
    background: linear-gradient(135deg, rgba(255,170,0,0.12), rgba(255,0,255,0.06));
    border: 1px solid rgba(255,170,0,0.5);
    border-radius: 12px;
    padding: 1rem 1.5rem;
    text-align: center;
    margin-bottom: 1.5rem;
  }
  .score-box h3 { color:#ffaa00; font-family:'Orbitron',monospace; font-size:1rem; margin:0; }
  .score-box .big-score { color:#ffffff; font-family:'Orbitron',monospace; font-size:2.5rem; font-weight:900; }

  /* ── Progress bar container ── */
  .progress-label { color:#00d4ff; font-size:0.85rem; letter-spacing:2px; text-transform:uppercase; margin-bottom:0.3rem; }
  div[data-testid="stProgress"] > div { border-radius:99px; }

  /* ── Player name display ── */
  .player-tag {
    text-align: center;
    font-family: 'Orbitron', monospace;
    color: #ffaa00;
    font-size: 0.85rem;
    letter-spacing: 2px;
    padding: 0.5rem;
    border-bottom: 1px solid rgba(255,170,0,0.3);
    margin-bottom: 1rem;
  }

  /* ── Final screen ── */
  .final-card {
    background: linear-gradient(135deg, rgba(0,212,255,0.08), rgba(255,0,255,0.06));
    border: 2px solid rgba(0,212,255,0.5);
    border-radius: 20px;
    padding: 3rem;
    text-align: center;
    box-shadow: 0 0 60px rgba(0,212,255,0.2);
    animation: fadeIn 0.8s ease;
  }
  @keyframes fadeIn { from{opacity:0;transform:translateY(20px)} to{opacity:1;transform:translateY(0)} }
  .final-card h1 { font-family:'Orbitron',monospace; color:#00ff88; font-size:2.2rem; text-shadow:0 0 30px #00ff88; }
  .final-card .final-score { font-family:'Orbitron',monospace; font-size:4rem; font-weight:900; color:#ffaa00; text-shadow:0 0 40px #ffaa00; }
  .final-card p { color:#aad4ff; font-size:1.1rem; }

  /* ── Section headers ── */
  .section-header {
    font-family: 'Rajdhani', sans-serif;
    color: #00d4ff;
    font-size: 0.8rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    border-bottom: 1px solid rgba(0,212,255,0.3);
    padding-bottom: 0.3rem;
    margin-bottom: 1rem;
  }

  /* ── Hint box ── */
  .hint-box {
    background: rgba(255,170,0,0.07);
    border: 1px solid rgba(255,170,0,0.3);
    border-radius: 8px;
    padding: 0.8rem 1rem;
    color: #ffcc66;
    font-size: 0.95rem;
    margin-top: 0.5rem;
  }
  
  /* ── Input styling ── */
  .stTextInput > div > div > input {
    background: rgba(0,212,255,0.05);
    border: 1px solid rgba(0,212,255,0.3);
    color: white;
    border-radius: 8px;
  }

  /* ─ hide default Streamlit elements ── */
  #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─── DATA LOADING ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    base = os.path.dirname(__file__)
    fin  = pd.read_csv(os.path.join(base, "data", "securite_financiere.csv"))
    fra  = pd.read_csv(os.path.join(base, "data", "apprentissage_francais.csv"))
    mon  = pd.read_csv(os.path.join(base, "data", "monuments_monde.csv"))
    return fin, fra, mon

fin_df, fra_df, mon_df = load_data()

# ─── SESSION STATE INIT ────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "screen": "home",          # home | quiz | result
        "player": "",
        "game_mode": None,
        "questions": [],
        "q_index": 0,
        "score": 0,
        "answer_given": False,
        "last_correct": None,
        "correct_answer": "",
        "total_q": 10,
        "wrong_answers": [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ─── HELPERS ───────────────────────────────────────────────────────────────────
MODES = {
    "🔐 Sécurité Financière": {
        "df": fin_df,
        "col_q": "Terme",
        "col_a": "Definition",
        "prompt": "Quelle est la définition de :",
        "color": "#00d4ff",
        "icon": "🏦",
        "desc": "Vocabulaire professionnel AML/KYC/Compliance"
    },
    "🇫🇷 Apprentissage du Français": {
        "df": fra_df,
        "col_q": "Mot_Expression",
        "col_a": "Definition_Synonyme",
        "prompt": "Synonyme ou définition de :",
        "color": "#ff00ff",
        "icon": "📚",
        "desc": "Vocabulaire, expressions et idiomes français"
    },
    "🏛️ Monuments du Monde": {
        "df": mon_df,
        "col_q": "Monument",
        "col_a": "Pays",
        "prompt": "Dans quel pays se trouve :",
        "color": "#ffaa00",
        "icon": "🌍",
        "desc": "Monuments historiques et leur pays d'origine"
    },
}

def build_questions(mode_cfg, n=10):
    df = mode_cfg["df"].dropna().sample(frac=1).reset_index(drop=True)
    qs = []
    for i in range(min(n, len(df))):
        row   = df.iloc[i]
        right = row[mode_cfg["col_a"]]
        wrong = df[df[mode_cfg["col_a"]] != right][mode_cfg["col_a"]].sample(3).tolist()
        choices = wrong + [right]
        random.shuffle(choices)
        qs.append({
            "question": row[mode_cfg["col_q"]],
            "correct":  right,
            "choices":  choices,
        })
    return qs

def get_badge(pct):
    if pct >= 90: return "🏆 LÉGENDAIRE", "#00ff88"
    if pct >= 70: return "⭐ EXPERT",     "#ffaa00"
    if pct >= 50: return "👍 BIEN",       "#00d4ff"
    return "📚 À REVOIR", "#ff4444"

def reset_quiz():
    for k in ["questions","q_index","score","answer_given","last_correct","correct_answer","wrong_answers"]:
        if k in ["questions","wrong_answers"]:
            st.session_state[k] = []
        elif k in ["q_index","score"]:
            st.session_state[k] = 0
        else:
            st.session_state[k] = None if k != "answer_given" else False

# ─── SCREEN: HOME ──────────────────────────────────────────────────────────────
def screen_home():
    st.markdown('<div class="main-title">⚡ QUIZ MASTER PRO</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Testez vos connaissances · Défiez vos limites</div>', unsafe_allow_html=True)

    col_l, col_c, col_r = st.columns([1,2,1])
    with col_c:
        with st.container():
            st.markdown('<div class="quiz-card">', unsafe_allow_html=True)

            st.markdown('<div class="section-header">👤 Votre identité</div>', unsafe_allow_html=True)
            player = st.text_input(
                "Nom du participant",
                value=st.session_state.player,
                placeholder="Entrez votre nom…",
                label_visibility="collapsed"
            )
            st.session_state.player = player

            st.markdown('<div class="section-header" style="margin-top:1.5rem">🎮 Choisissez votre univers</div>', unsafe_allow_html=True)

            for mode_name, cfg in MODES.items():
                cols = st.columns([3,1])
                with cols[0]:
                    st.markdown(
                        f'<div style="color:{cfg["color"]};font-weight:700;font-size:1.05rem">{cfg["icon"]} {mode_name.split(" ",1)[1]}</div>'
                        f'<div style="color:#aaa;font-size:0.82rem;margin-bottom:0.3rem">{cfg["desc"]}</div>',
                        unsafe_allow_html=True
                    )
                with cols[1]:
                    if st.button("JOUER", key=f"btn_{mode_name}"):
                        if not player.strip():
                            st.warning("⚠️ Entrez votre nom pour jouer !")
                        else:
                            reset_quiz()
                            st.session_state.game_mode  = mode_name
                            st.session_state.questions  = build_questions(cfg, st.session_state.total_q)
                            st.session_state.screen     = "quiz"
                            st.rerun()
                st.divider()

            st.markdown('<div class="section-header">⚙️ Nombre de questions</div>', unsafe_allow_html=True)
            n = st.slider("", 5, 20, st.session_state.total_q, label_visibility="collapsed")
            st.session_state.total_q = n

            st.markdown('</div>', unsafe_allow_html=True)

    # Stats row
    c1,c2,c3 = st.columns(3)
    with c1:
        st.markdown('<div class="quiz-card" style="text-align:center"><div style="font-size:2rem">🔐</div>'
                    f'<div style="color:#00d4ff;font-family:Orbitron;font-size:0.8rem">FINANCE</div>'
                    f'<div style="color:#fff;font-size:1.4rem;font-weight:700">{len(fin_df)} termes</div></div>',
                    unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="quiz-card" style="text-align:center"><div style="font-size:2rem">🇫🇷</div>'
                    f'<div style="color:#ff00ff;font-family:Orbitron;font-size:0.8rem">FRANÇAIS</div>'
                    f'<div style="color:#fff;font-size:1.4rem;font-weight:700">{len(fra_df)} mots</div></div>',
                    unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="quiz-card" style="text-align:center"><div style="font-size:2rem">🏛️</div>'
                    f'<div style="color:#ffaa00;font-family:Orbitron;font-size:0.8rem">MONUMENTS</div>'
                    f'<div style="color:#fff;font-size:1.4rem;font-weight:700">{len(mon_df)} monuments</div></div>',
                    unsafe_allow_html=True)


# ─── SCREEN: QUIZ ──────────────────────────────────────────────────────────────
def screen_quiz():
    mode_cfg = MODES[st.session_state.game_mode]
    qs       = st.session_state.questions
    qi       = st.session_state.q_index
    total    = len(qs)

    if qi >= total:
        st.session_state.screen = "result"
        st.rerun()
        return

    q = qs[qi]

    # ── Sidebar ──
    with st.sidebar:
        st.markdown(f'<div class="player-tag">👤 {st.session_state.player.upper()}</div>', unsafe_allow_html=True)

        st.markdown('<div class="score-box">'
                    '<h3>⚡ SCORE</h3>'
                    f'<div class="big-score">{st.session_state.score}/{qi}</div>'
                    '</div>', unsafe_allow_html=True)

        pct = int(qi/total*100) if total else 0
        st.markdown(f'<div class="progress-label">📊 Progression — {qi}/{total}</div>', unsafe_allow_html=True)
        st.progress(qi/total if total else 0)

        st.markdown(f"""
        <div style="margin-top:1rem;color:#aaa;font-size:0.85rem">
        <div>🎮 Mode : <span style="color:{mode_cfg['color']}">{st.session_state.game_mode.split(' ',1)[1]}</span></div>
        <div>❓ Question : <span style="color:#fff">{qi+1}/{total}</span></div>
        <div>✅ Bonnes : <span style="color:#00ff88">{st.session_state.score}</span></div>
        <div>❌ Mauvaises : <span style="color:#ff4444">{qi - st.session_state.score}</span></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        if st.button("🏠 Accueil"):
            st.session_state.screen = "home"
            st.rerun()

    # ── Main ──
    st.markdown(f'<div class="main-title" style="font-size:1.8rem">{mode_cfg["icon"]} {st.session_state.game_mode.split(" ",1)[1]}</div>', unsafe_allow_html=True)

    # Progress bar top
    prog_pct = qi/total if total else 0
    st.progress(prog_pct)
    st.markdown(f'<div style="text-align:center;color:#00d4ff99;font-size:0.8rem;letter-spacing:2px">QUESTION {qi+1} / {total}</div>', unsafe_allow_html=True)

    st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="question-text">{mode_cfg["prompt"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="term-display">{q["question"]}</div>', unsafe_allow_html=True)

    # ── Answer notification ──
    if st.session_state.answer_given:
        if st.session_state.last_correct:
            st.markdown(f"""
            <div class="notif-correct">
              <h2>✅ CORRECT !</h2>
              <p>Réponse : <strong style="color:#00ff88">{q['correct']}</strong></p>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="notif-wrong">
              <h2>❌ INCORRECT</h2>
              <p>La bonne réponse était : <strong style="color:#ff4444">{q['correct']}</strong></p>
            </div>""", unsafe_allow_html=True)

        if st.button("➡️ Question suivante", use_container_width=True):
            st.session_state.q_index    += 1
            st.session_state.answer_given = False
            st.session_state.last_correct = None
            st.rerun()

    else:
        # ── Choice buttons ──
        cols = st.columns(2)
        for idx, choice in enumerate(q["choices"]):
            with cols[idx % 2]:
                label = f"{'ABCD'[idx]}  {choice}"
                if st.button(label, key=f"choice_{qi}_{idx}", use_container_width=True):
                    correct = (choice == q["correct"])
                    st.session_state.answer_given = True
                    st.session_state.last_correct = correct
                    if correct:
                        st.session_state.score += 1
                    else:
                        st.session_state.wrong_answers.append({
                            "question": q["question"],
                            "votre_reponse": choice,
                            "bonne_reponse": q["correct"]
                        })
                    st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


# ─── SCREEN: RESULT ────────────────────────────────────────────────────────────
def screen_result():
    total  = len(st.session_state.questions)
    score  = st.session_state.score
    pct    = int(score/total*100) if total else 0
    badge, badge_color = get_badge(pct)
    mode   = st.session_state.game_mode
    player = st.session_state.player

    with st.sidebar:
        if st.button("🏠 Accueil"):
            st.session_state.screen = "home"
            st.rerun()
        if st.button("🔄 Rejouer"):
            cfg = MODES[mode]
            reset_quiz()
            st.session_state.questions = build_questions(cfg, st.session_state.total_q)
            st.session_state.screen    = "quiz"
            st.rerun()

    col_l, col_c, col_r = st.columns([1,3,1])
    with col_c:
        st.markdown(f"""
        <div class="final-card">
          <h1>🎯 RÉSULTATS FINAUX</h1>
          <div style="color:#00d4ffaa;font-family:Orbitron;font-size:0.85rem;letter-spacing:3px;margin:0.5rem 0">
            {player.upper()}
          </div>
          <div class="final-score">{score} / {total}</div>
          <div style="font-size:2rem;margin:0.5rem 0">{int(pct)}%</div>
          <div style="color:{badge_color};font-family:Orbitron;font-size:1.4rem;font-weight:700;
                       text-shadow:0 0 20px {badge_color};margin:1rem 0">
            {badge}
          </div>
          <p>Mode : {mode}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # Progress details
        c1,c2,c3 = st.columns(3)
        with c1:
            st.markdown(f'<div class="quiz-card" style="text-align:center"><div style="color:#00ff88;font-size:2rem">✅</div>'
                        f'<div style="color:#00ff88;font-family:Orbitron;font-size:1.5rem">{score}</div>'
                        f'<div style="color:#aaa;font-size:0.8rem">BONNES</div></div>',
                        unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="quiz-card" style="text-align:center"><div style="color:#ff4444;font-size:2rem">❌</div>'
                        f'<div style="color:#ff4444;font-family:Orbitron;font-size:1.5rem">{total-score}</div>'
                        f'<div style="color:#aaa;font-size:0.8rem">MAUVAISES</div></div>',
                        unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="quiz-card" style="text-align:center"><div style="color:#ffaa00;font-size:2rem">📊</div>'
                        f'<div style="color:#ffaa00;font-family:Orbitron;font-size:1.5rem">{pct}%</div>'
                        f'<div style="color:#aaa;font-size:0.8rem">PRÉCISION</div></div>',
                        unsafe_allow_html=True)

        # Wrong answers review
        if st.session_state.wrong_answers:
            st.markdown("---")
            st.markdown('<div class="section-header">📖 Révision — Réponses incorrectes</div>', unsafe_allow_html=True)
            for wa in st.session_state.wrong_answers:
                st.markdown(f"""
                <div class="quiz-card" style="padding:1rem;margin:0.4rem 0;border-color:rgba(255,68,68,0.3)">
                  <div style="color:#00d4ff;font-weight:700">{wa['question']}</div>
                  <div style="color:#ff8888;font-size:0.9rem">Votre réponse : {wa['votre_reponse']}</div>
                  <div style="color:#00ff88;font-size:0.9rem">✅ Bonne réponse : {wa['bonne_reponse']}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🔄 Rejouer ce mode", use_container_width=True):
                cfg = MODES[mode]
                reset_quiz()
                st.session_state.questions = build_questions(cfg, st.session_state.total_q)
                st.session_state.screen    = "quiz"
                st.rerun()
        with col_b:
            if st.button("🏠 Changer de mode", use_container_width=True):
                st.session_state.screen = "home"
                st.rerun()

# ─── ROUTER ────────────────────────────────────────────────────────────────────
if st.session_state.screen == "home":
    screen_home()
elif st.session_state.screen == "quiz":
    screen_quiz()
elif st.session_state.screen == "result":
    screen_result()
