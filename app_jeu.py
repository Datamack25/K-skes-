"""
⚡ Quiz Master Pro v4
Fixes: sidebar nav everywhere, retour accueil, code salle visible,
       boutons niveau cliquables, phrase dans barre nom,
       +10s timers, animations, date accueil, lien salle fonctionnel
"""

import streamlit as st
import pandas as pd
import random, time, os, json, hashlib, glob
from datetime import datetime

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="⚡ Quiz Master Pro",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
#  MEGA CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&display=swap');

/* ── Reset & base ── */
html,body,[class*="css"]{font-family:'Rajdhani',sans-serif;}

/* ── Background: animated mesh + particles ── */
.stApp{
  background:
    radial-gradient(ellipse 80% 60% at 20% 10%, rgba(0,212,255,.06) 0%, transparent 60%),
    radial-gradient(ellipse 60% 50% at 80% 80%, rgba(255,0,255,.05) 0%, transparent 55%),
    radial-gradient(ellipse 50% 40% at 50% 50%, rgba(0,255,136,.03) 0%, transparent 60%),
    linear-gradient(160deg, #030312 0%, #07091e 40%, #030b18 100%);
  min-height:100vh;
  overflow-x:hidden;
}

/* ── Floating grid overlay ── */
.stApp::before{
  content:'';
  position:fixed;inset:0;
  background-image:
    linear-gradient(rgba(0,212,255,.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,212,255,.04) 1px, transparent 1px);
  background-size:60px 60px;
  pointer-events:none;z-index:0;
}

/* ── Sidebar ── */
[data-testid="stSidebar"]{
  background:linear-gradient(180deg,#08091c 0%,#040410 100%);
  border-right:1px solid rgba(0,212,255,.15);
  box-shadow:4px 0 30px rgba(0,0,0,.6);
}
[data-testid="stSidebar"] .stButton>button{
  background:linear-gradient(135deg,rgba(0,212,255,.08),rgba(0,0,0,.6));
  border:1px solid rgba(0,212,255,.25);
  color:#c8eeff;margin-bottom:.3rem;
}
[data-testid="stSidebar"] .stButton>button:hover{
  background:linear-gradient(135deg,rgba(0,212,255,.18),rgba(255,0,255,.08));
  border-color:#00d4ff;color:#fff;
  box-shadow:0 0 15px rgba(0,212,255,.3);
}

/* ── Title ── */
.main-title{
  font-family:'Orbitron',monospace;font-weight:900;text-align:center;
  background:linear-gradient(90deg,#00d4ff,#ff00ff,#00ff88,#ffaa00,#ff3388,#00d4ff);
  background-size:500%;
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  animation:gs 6s ease infinite;
  filter:drop-shadow(0 0 20px rgba(0,212,255,.25));
}
@keyframes gs{0%,100%{background-position:0%}50%{background-position:100%}}
.subtitle{text-align:center;color:#00d4ff55;font-size:.78rem;letter-spacing:5px;text-transform:uppercase;}

/* ── Cards ── */
.card{
  background:linear-gradient(135deg,rgba(0,212,255,.05),rgba(255,0,255,.03),rgba(0,0,0,.4));
  border:1px solid rgba(0,212,255,.2);border-radius:18px;
  padding:1.4rem;margin:.6rem 0;
  box-shadow:0 0 25px rgba(0,212,255,.06),0 4px 20px rgba(0,0,0,.4),inset 0 0 20px rgba(0,0,0,.2);
  position:relative;overflow:hidden;
}
.card::before{
  content:'';position:absolute;top:-50%;left:-50%;
  width:200%;height:200%;
  background:conic-gradient(from 180deg at 50% 50%,transparent 0deg,rgba(0,212,255,.02) 60deg,transparent 120deg);
  animation:rotate 12s linear infinite;
}
@keyframes rotate{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}

/* ── Question card ── */
.q-card{
  background:linear-gradient(135deg,rgba(0,212,255,.08),rgba(0,0,0,.65));
  border:1px solid rgba(0,212,255,.55);border-radius:16px;
  padding:2rem;text-align:center;margin:1rem 0;
  box-shadow:0 0 35px rgba(0,212,255,.18),0 0 70px rgba(0,212,255,.04);
  position:relative;overflow:hidden;
}
.q-card::after{
  content:'';position:absolute;bottom:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,transparent,#00d4ff,#ff00ff,#00ff88,transparent);
  animation:scan 3s ease infinite;
}
@keyframes scan{0%,100%{opacity:.4}50%{opacity:1}}
.q-prompt{font-family:'Orbitron',monospace;font-size:.9rem;color:#88ccff;letter-spacing:2px;margin-bottom:.6rem;}
.q-term{
  font-family:'Orbitron',monospace;font-size:1.4rem;font-weight:900;
  color:#00ff88;line-height:1.5;margin:.5rem 0;
  text-shadow:0 0 25px rgba(0,255,136,.6),0 0 50px rgba(0,255,136,.2);
  animation:pulse-green 3s ease infinite;
}
@keyframes pulse-green{0%,100%{text-shadow:0 0 25px rgba(0,255,136,.6)}50%{text-shadow:0 0 40px rgba(0,255,136,.9),0 0 80px rgba(0,255,136,.3)}}

/* ── Timer ── */
.timer{text-align:center;padding:.55rem 1.2rem;border-radius:50px;display:inline-block;
  font-family:'Orbitron',monospace;font-size:1.3rem;font-weight:900;transition:all .3s;}
.t-green{background:rgba(0,255,136,.1);border:2px solid #00ff88;color:#00ff88;
  box-shadow:0 0 20px rgba(0,255,136,.3),inset 0 0 10px rgba(0,255,136,.05);}
.t-yellow{background:rgba(255,170,0,.1);border:2px solid #ffaa00;color:#ffaa00;
  box-shadow:0 0 20px rgba(255,170,0,.3);}
.t-red{background:rgba(255,50,50,.12);border:2px solid #ff4444;color:#ff4444;
  box-shadow:0 0 25px rgba(255,68,68,.45);animation:blink .45s infinite;}
@keyframes blink{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.3;transform:scale(.97)}}

/* ── LEVEL BUTTONS (real clickable buttons) ── */
.lvl-btn{
  display:block;width:100%;padding:.75rem .5rem;
  border-radius:12px;text-align:center;cursor:pointer;
  font-family:'Orbitron',monospace;font-weight:700;font-size:.72rem;
  letter-spacing:1px;line-height:1.5;
  transition:all .25s cubic-bezier(.34,1.56,.64,1);
  position:relative;overflow:hidden;
  text-decoration:none;user-select:none;
}
.lvl-btn::before{
  content:'';position:absolute;inset:0;opacity:0;
  background:radial-gradient(circle at 50% 50%,rgba(255,255,255,.15),transparent 70%);
  transition:opacity .2s;
}
.lvl-btn:hover::before{opacity:1;}
.lvl-btn:hover{transform:translateY(-3px) scale(1.03);}
.lvl-btn:active{transform:translateY(0) scale(.97);}

.lvl-debutant{
  background:linear-gradient(135deg,rgba(0,212,255,.15),rgba(0,100,180,.1));
  border:2px solid #00d4ff;color:#00d4ff;
  box-shadow:0 0 15px rgba(0,212,255,.2),0 4px 12px rgba(0,0,0,.5);
}
.lvl-debutant.active{
  background:linear-gradient(135deg,rgba(0,212,255,.35),rgba(0,150,220,.2));
  box-shadow:0 0 30px rgba(0,212,255,.6),0 0 60px rgba(0,212,255,.2),0 4px 15px rgba(0,0,0,.5);
  border-color:#00d4ff;transform:scale(1.04);
}
.lvl-potentiel{
  background:linear-gradient(135deg,rgba(0,255,136,.15),rgba(0,150,80,.1));
  border:2px solid #00ff88;color:#00ff88;
  box-shadow:0 0 15px rgba(0,255,136,.2),0 4px 12px rgba(0,0,0,.5);
}
.lvl-potentiel.active{
  background:linear-gradient(135deg,rgba(0,255,136,.35),rgba(0,200,100,.2));
  box-shadow:0 0 30px rgba(0,255,136,.6),0 0 60px rgba(0,255,136,.2),0 4px 15px rgba(0,0,0,.5);
  transform:scale(1.04);
}
.lvl-legende{
  background:linear-gradient(135deg,rgba(255,170,0,.15),rgba(180,80,0,.1));
  border:2px solid #ffaa00;color:#ffaa00;
  box-shadow:0 0 15px rgba(255,170,0,.2),0 4px 12px rgba(0,0,0,.5);
}
.lvl-legende.active{
  background:linear-gradient(135deg,rgba(255,170,0,.35),rgba(220,120,0,.2));
  box-shadow:0 0 30px rgba(255,170,0,.6),0 0 60px rgba(255,170,0,.2),0 4px 15px rgba(0,0,0,.5);
  transform:scale(1.04);
}
.lvl-superstar{
  background:linear-gradient(135deg,rgba(255,0,255,.15),rgba(150,0,180,.1));
  border:2px solid #ff00ff;color:#ff00ff;
  box-shadow:0 0 15px rgba(255,0,255,.2),0 4px 12px rgba(0,0,0,.5);
}
.lvl-superstar.active{
  background:linear-gradient(135deg,rgba(255,0,255,.35),rgba(200,0,220,.2));
  box-shadow:0 0 30px rgba(255,0,255,.6),0 0 60px rgba(255,0,255,.2),0 4px 15px rgba(0,0,0,.5);
  transform:scale(1.04);
}

/* ── Notifications ── */
.notif{border-radius:16px;padding:1.6rem;text-align:center;margin:1rem 0;position:relative;overflow:hidden;}
.notif::after{content:'';position:absolute;bottom:0;left:0;right:0;height:3px;
  background:linear-gradient(90deg,transparent,currentColor,transparent);}
.n-ok{
  background:linear-gradient(135deg,rgba(0,255,136,.12),rgba(0,180,80,.05));
  border:2px solid #00ff88;
  box-shadow:0 0 50px rgba(0,255,136,.35),0 0 100px rgba(0,255,136,.1);
  animation:popIn .4s cubic-bezier(.34,1.56,.64,1);
}
.n-wrong{
  background:linear-gradient(135deg,rgba(255,50,50,.12),rgba(180,0,0,.05));
  border:2px solid #ff4444;
  box-shadow:0 0 50px rgba(255,68,68,.35),0 0 100px rgba(255,68,68,.1);
  animation:shake .45s ease;
}
.n-time{
  background:linear-gradient(135deg,rgba(255,170,0,.12),rgba(180,80,0,.05));
  border:2px solid #ffaa00;
  box-shadow:0 0 50px rgba(255,170,0,.35);
  animation:popIn .4s ease;
}
@keyframes popIn{0%{transform:scale(.65);opacity:0}70%{transform:scale(1.06)}100%{transform:scale(1);opacity:1}}
@keyframes shake{0%,100%{transform:translateX(0)}20%{transform:translateX(-10px)}40%{transform:translateX(10px)}60%{transform:translateX(-7px)}80%{transform:translateX(7px)}}
.notif h2{font-family:'Orbitron',monospace;font-size:1.4rem;margin:0;}
.n-ok  h2{color:#00ff88;text-shadow:0 0 20px #00ff88;}
.n-wrong h2{color:#ff4444;text-shadow:0 0 20px #ff4444;}
.n-time h2{color:#ffaa00;text-shadow:0 0 20px #ffaa00;}
.notif p{color:#ccc;font-size:.95rem;margin:.4rem 0 0;}

/* ── Score box ── */
.score-box{
  background:linear-gradient(135deg,rgba(255,170,0,.1),rgba(255,0,255,.05));
  border:1px solid rgba(255,170,0,.4);border-radius:12px;
  padding:.9rem;text-align:center;margin-bottom:.8rem;
  box-shadow:0 0 20px rgba(255,170,0,.08);
}
.score-box h3{color:#ffaa00;font-family:'Orbitron',monospace;font-size:.72rem;margin:0;letter-spacing:2px;}
.score-box .big{color:#fff;font-family:'Orbitron',monospace;font-size:2rem;font-weight:900;
  text-shadow:0 0 20px rgba(255,170,0,.4);}

/* ── Room code display ── */
.room-display{
  background:linear-gradient(135deg,rgba(0,212,255,.1),rgba(0,255,136,.05));
  border:2px solid rgba(0,212,255,.5);border-radius:16px;
  padding:1.4rem;text-align:center;margin:1rem 0;
  box-shadow:0 0 40px rgba(0,212,255,.2),0 0 80px rgba(0,212,255,.06);
  animation:popIn .5s ease;
}
.room-code-big{
  font-family:'Orbitron',monospace;font-size:3rem;font-weight:900;
  color:#00d4ff;letter-spacing:8px;
  text-shadow:0 0 30px rgba(0,212,255,.8),0 0 60px rgba(0,212,255,.3);
  animation:pulse-blue 2s ease infinite;
}
@keyframes pulse-blue{0%,100%{text-shadow:0 0 30px rgba(0,212,255,.8)}50%{text-shadow:0 0 50px rgba(0,212,255,1),0 0 100px rgba(0,212,255,.5)}}
.room-lbl{font-size:.65rem;color:#00d4ff77;letter-spacing:4px;text-transform:uppercase;margin:.3rem 0;}

/* ── Sidebar room badge ── */
.sb-room{
  background:rgba(0,212,255,.07);border:1px solid rgba(0,212,255,.35);
  border-radius:10px;padding:.65rem;text-align:center;margin:.5rem 0;
  font-family:'Orbitron',monospace;
}
.sb-room-code{font-size:1.4rem;font-weight:900;color:#00d4ff;letter-spacing:4px;
  text-shadow:0 0 15px rgba(0,212,255,.6);}
.sb-room-lbl{font-size:.55rem;color:#00d4ff66;letter-spacing:3px;text-transform:uppercase;}

/* ── Player rows ── */
.p-row{
  display:flex;align-items:center;gap:.7rem;
  background:rgba(0,212,255,.04);border:1px solid rgba(0,212,255,.15);
  border-radius:10px;padding:.55rem .85rem;margin:.28rem 0;transition:all .2s;
}
.p-row.me{border-color:#00ff88;box-shadow:0 0 12px rgba(0,255,136,.15);}
.p-dot{width:10px;height:10px;border-radius:50%;flex-shrink:0;}
.p-name{color:#e0f0ff;font-weight:600;flex:1;font-size:.88rem;}
.p-name.me{color:#00ff88;}
.p-score{color:#ffaa00;font-family:'Orbitron',monospace;font-weight:700;font-size:.9rem;}

/* ── Stat cards ── */
.stat-card{
  text-align:center;padding:1rem;border-radius:14px;
  background:linear-gradient(135deg,rgba(0,0,0,.4),rgba(0,212,255,.03));
  border:1px solid rgba(0,212,255,.15);transition:all .3s;
  box-shadow:0 4px 15px rgba(0,0,0,.4);
}
.stat-card:hover{transform:translateY(-3px);box-shadow:0 8px 25px rgba(0,0,0,.5);}

/* ── Final screen ── */
.final{
  background:linear-gradient(135deg,rgba(0,212,255,.08),rgba(255,0,255,.05),rgba(0,0,0,.5));
  border:2px solid rgba(0,212,255,.4);border-radius:22px;
  padding:2.6rem;text-align:center;
  box-shadow:0 0 60px rgba(0,212,255,.15),0 0 120px rgba(0,212,255,.04);
  animation:popIn .7s ease;position:relative;overflow:hidden;
}
.final::before{
  content:'🎉';position:absolute;font-size:8rem;opacity:.03;
  top:50%;left:50%;transform:translate(-50%,-50%);
}
.final h1{font-family:'Orbitron',monospace;color:#00ff88;font-size:1.9rem;
  text-shadow:0 0 25px #00ff88;margin-bottom:.4rem;}
.f-score{font-family:'Orbitron',monospace;font-size:3.2rem;font-weight:900;
  color:#ffaa00;text-shadow:0 0 35px #ffaa00;}

/* ── Date banner ── */
.date-banner{
  text-align:center;font-family:'Orbitron',monospace;font-size:.75rem;
  color:#00d4ff44;letter-spacing:3px;text-transform:uppercase;margin-bottom:.5rem;
}

/* ── Motivation bar ── */
.motive-bar{
  background:linear-gradient(135deg,rgba(255,170,0,.08),rgba(255,0,255,.05));
  border:1px solid rgba(255,170,0,.25);border-radius:10px;
  padding:.7rem 1.2rem;text-align:center;margin:.4rem 0;
  font-family:'Orbitron',monospace;font-size:.78rem;
  color:#ffcc66;letter-spacing:1px;
  animation:glowpulse 4s ease infinite;
}
@keyframes glowpulse{0%,100%{box-shadow:0 0 10px rgba(255,170,0,.1)}50%{box-shadow:0 0 25px rgba(255,170,0,.25)}}

/* ── Progress bar custom ── */
.prog-wrap{
  background:rgba(255,255,255,.06);border-radius:99px;
  height:6px;margin:.5rem 0;overflow:hidden;
  border:1px solid rgba(0,212,255,.15);
}
.prog-fill{
  height:100%;border-radius:99px;
  background:linear-gradient(90deg,#00d4ff,#00ff88,#ffaa00);
  transition:width .5s ease;
  box-shadow:0 0 8px rgba(0,212,255,.5);
}

/* ── Name input placeholder ── */
.stTextInput>div>div>input{
  background:rgba(0,212,255,.04);
  border:1px solid rgba(0,212,255,.3);
  color:white;border-radius:10px;
  font-family:'Rajdhani',sans-serif;font-size:1.1rem;
  padding:.7rem 1rem;
}
.stTextInput>div>div>input::placeholder{color:rgba(0,212,255,.4);}

/* ── Answer buttons glow on hover ── */
.stButton>button{
  width:100%;padding:.85rem 1rem;
  font-family:'Rajdhani',sans-serif;font-size:1rem;font-weight:600;
  border-radius:12px;border:1px solid rgba(0,212,255,.3);
  background:linear-gradient(135deg,rgba(0,212,255,.07),rgba(0,0,0,.55));
  color:#dff0ff;cursor:pointer;transition:all .2s ease;
  position:relative;overflow:hidden;
}
.stButton>button::before{
  content:'';position:absolute;inset:0;opacity:0;
  background:radial-gradient(circle at 50% 50%,rgba(0,212,255,.12),transparent 70%);
  transition:opacity .2s;
}
.stButton>button:hover::before{opacity:1;}
.stButton>button:hover{
  background:linear-gradient(135deg,rgba(0,212,255,.16),rgba(255,0,255,.07));
  border-color:#00d4ff;color:#fff;
  box-shadow:0 0 20px rgba(0,212,255,.3),0 0 40px rgba(0,212,255,.08);
  transform:translateY(-2px);
}
.stButton>button:active{transform:translateY(0);}

/* ── Section header ── */
.hdr{
  color:#00d4ff;font-size:.7rem;letter-spacing:3px;text-transform:uppercase;
  border-bottom:1px solid rgba(0,212,255,.2);padding-bottom:.25rem;margin:1rem 0 .7rem;
  display:flex;align-items:center;gap:.5rem;
}
.hdr::before{content:'';flex:1;height:1px;background:linear-gradient(90deg,rgba(0,212,255,.3),transparent);}
.hdr::after{content:'';flex:1;height:1px;background:linear-gradient(270deg,rgba(0,212,255,.3),transparent);}

/* ── Player tag ── */
.p-tag{text-align:center;font-family:'Orbitron',monospace;color:#ffaa00;
  font-size:.75rem;letter-spacing:2px;padding:.4rem;
  border-bottom:1px solid rgba(255,170,0,.2);margin-bottom:.7rem;}

/* ── Decorative corner accents ── */
.corner-deco{
  position:relative;padding:1.5rem;
}
.corner-deco::before,.corner-deco::after{
  content:'';position:absolute;width:20px;height:20px;
}
.corner-deco::before{top:0;left:0;border-top:2px solid #00d4ff;border-left:2px solid #00d4ff;}
.corner-deco::after{bottom:0;right:0;border-bottom:2px solid #ff00ff;border-right:2px solid #ff00ff;}

/* ── Scrollbar ── */
::-webkit-scrollbar{width:6px;}
::-webkit-scrollbar-track{background:rgba(0,0,0,.3);}
::-webkit-scrollbar-thumb{background:rgba(0,212,255,.3);border-radius:3px;}

#MainMenu,footer,header{visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════
BASE      = os.path.dirname(os.path.abspath(__file__))
DATA_DIR  = os.path.join(BASE, "data")
ROOMS_DIR = os.path.join(BASE, "rooms")
os.makedirs(ROOMS_DIR, exist_ok=True)

PLAYER_COLORS = ["#00d4ff","#ff00ff","#00ff88","#ffaa00"]

# +10s vs v3 on every level
LEVELS = {
    "🌱 Débutant":  {"key":"debutant",  "time":40, "qs":10, "color":"#00d4ff", "mult":1,  "css":"lvl-debutant"},
    "⚡ Potentiel": {"key":"potentiel", "time":30, "qs":15, "color":"#00ff88", "mult":2,  "css":"lvl-potentiel"},
    "🔥 Légende":   {"key":"legende",   "time":25, "qs":20, "color":"#ffaa00", "mult":3,  "css":"lvl-legende"},
    "👑 Superstar": {"key":"superstar", "time":20, "qs":25, "color":"#ff00ff", "mult":5,  "css":"lvl-superstar"},
}

MODES = {
    "🔐 Sécurité Financière": {"file":"securite_financiere.csv","type":"vocab","col_q":"Terme","col_a":"Definition","prompt":"Quelle est la définition de :","color":"#00d4ff","icon":"🏦","desc":"Vocabulaire AML/KYC/Compliance"},
    "🇫🇷 Français":           {"file":"apprentissage_francais.csv","type":"vocab","col_q":"Mot_Expression","col_a":"Definition_Synonyme","prompt":"Synonyme ou définition de :","color":"#ff00ff","icon":"📚","desc":"Vocabulaire & expressions françaises"},
    "🇬🇧 Anglais":            {"file":"anglais.csv","type":"vocab","col_q":"Mot_Expression","col_a":"Definition_EN","prompt":"What is the definition of:","color":"#00ffff","icon":"🌐","desc":"English vocabulary and idioms"},
    "🇪🇸 Espagnol":           {"file":"espagnol.csv","type":"vocab","col_q":"Mot_Expression","col_a":"Definition_ES","prompt":"¿Cuál es la definición de:","color":"#ff6600","icon":"🌮","desc":"Vocabulario y expresiones en español"},
    "🇭🇹 Créole Haïtien":     {"file":"creole_haitien.csv","type":"vocab","col_q":"Mot_Expression","col_a":"Definition_Kreyol","prompt":"Ki definisyon oswa sinonim:","color":"#ff0044","icon":"🌴","desc":"Mo ak ekspresyon an kreyòl ayisyen"},
    "🏛️ Monuments":           {"file":"monuments_monde.csv","type":"vocab","col_q":"Monument","col_a":"Pays","prompt":"Dans quel pays se trouve :","color":"#ffaa00","icon":"🌍","desc":"Monuments historiques du monde entier"},
    "🎵 Musique":             {"file":"musique_monde.csv","type":"music","col_q":"Artiste","col_a":"Chanson","prompt":"Quelle est la chanson de :","color":"#ff00aa","icon":"🎶","desc":"Artistes & chansons haïtiens et mondiaux"},
    "🔢 Mathématiques":       {"file":"mathematiques.csv","type":"math","col_q":"Question","col_a":"Reponse","prompt":"Résolvez :","color":"#00ff88","icon":"🧮","desc":"Algèbre et calcul — tous niveaux"},
    "🏺 Histoire":            {"file":"histoire.csv","type":"mcq","col_q":"Question","col_a":"Reponse_Correcte","prompt":"","color":"#ff8800","icon":"📜","desc":"France · Haïti · Histoire mondiale"},
    "🌐 Culture Générale":    {"file":"culture_generale.csv","type":"mcq","col_q":"Question","col_a":"Reponse_Correcte","prompt":"","color":"#aa00ff","icon":"🧠","desc":"Sciences · Géo · Art · Sports"},
}

MOTIVATIONS = [
    "🔥 Prouve ce que tu vaux — le podium n'attend que toi !",
    "⚡ Chaque bonne réponse te rapproche de la légende.",
    "🏆 Les champions ne naissent pas — ils s'entraînent ici.",
    "🧠 Plus tu joues, plus tu brilles. En avant !",
    "🌟 Ta prochaine victoire commence maintenant.",
    "🚀 Le savoir est une arme. Affûte la tienne.",
    "💡 Curieux aujourd'hui, expert demain.",
    "🎯 Vise haut — les étoiles sont à portée de clic !",
]

# ══════════════════════════════════════════════════════════════════════════════
#  DATA LOADING (unlimited)
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data(ttl=60)
def load_csv(filename: str) -> pd.DataFrame:
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return pd.DataFrame()
    for enc in ("utf-8-sig","utf-8","latin-1"):
        try:
            df = pd.read_csv(path, encoding=enc, on_bad_lines="skip", dtype=str, skip_blank_lines=True)
            df = df.loc[:, ~df.columns.str.startswith("Unnamed")]
            df.columns = [c.strip() for c in df.columns]
            return df.dropna(how="all")
        except Exception:
            continue
    return pd.DataFrame()

def get_df(m): return load_csv(MODES[m]["file"])
def csv_count(m): return len(get_df(m))

# ══════════════════════════════════════════════════════════════════════════════
#  QUESTION BUILDER
# ══════════════════════════════════════════════════════════════════════════════
def build_questions(mode_name, level_key, n):
    cfg = MODES[mode_name]
    df  = get_df(mode_name)
    if df.empty: return []
    cq, ca = cfg["col_q"], cfg["col_a"]
    if cq not in df.columns or ca not in df.columns:
        st.error(f"⚠️ Colonnes manquantes dans {cfg['file']} : '{cq}' et '{ca}' requis.")
        return []
    df = df.dropna(subset=[cq,ca]).copy()
    df[cq] = df[cq].astype(str).str.strip()
    df[ca] = df[ca].astype(str).str.strip()
    df = df[df[cq] != ""]
    order = ["debutant","potentiel","legende","superstar"]
    if cfg["type"] in ("math","mcq") and "Difficulte" in df.columns:
        allowed = order[:order.index(level_key)+1]
        sub = df[df["Difficulte"].isin(allowed)]
        if len(sub) > 0: df = sub
    df = df.sample(frac=1, random_state=random.randint(0,9999)).reset_index(drop=True)
    n = min(n, len(df))
    if n == 0: return []
    qs = []
    for i in range(n):
        row, right = df.iloc[i], str(df.iloc[i][ca]).strip()
        if cfg["type"] == "mcq":
            choices = [right]
            for cx in ["Choix_2","Choix_3","Choix_4"]:
                if cx in df.columns:
                    v = str(row.get(cx,"")).strip()
                    if v and v != "nan" and v not in choices: choices.append(v)
            pool = [str(x).strip() for x in df[df[ca]!=right][ca].dropna().tolist() if str(x).strip() != "nan"]
            random.shuffle(pool)
            for p in pool:
                if len(choices) >= 4: break
                if p not in choices: choices.append(p)
            choices = choices[:4]
        else:
            pool = [str(x).strip() for x in df[df[ca]!=right][ca].dropna().tolist() if str(x).strip() not in ("nan","")]
            random.shuffle(pool)
            choices = [right] + pool[:3]
        random.shuffle(choices)
        qs.append({"question":str(row[cq]).strip(),"correct":right,"choices":choices,"prompt":cfg["prompt"]})
    return qs

# ══════════════════════════════════════════════════════════════════════════════
#  ROOM SYSTEM
# ══════════════════════════════════════════════════════════════════════════════
ROOM_TTL = 7200

def _rpath(code): return os.path.join(ROOMS_DIR, f"room_{code.upper()}.json")

def gen_code():
    return hashlib.md5(str(time.time()+random.random()).encode()).hexdigest()[:6].upper()

def room_save(code, data):
    with open(_rpath(code), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

def room_load(code):
    p = _rpath(code)
    if not os.path.exists(p): return None
    try:
        with open(p, encoding="utf-8") as f: data = json.load(f)
        if time.time() - data.get("created",0) > ROOM_TTL:
            os.remove(p); return None
        return data
    except: return None

def room_create(code, host, mode, level, questions):
    data = {
        "code":code,"host":host,"mode":mode,"level":level,
        "created":time.time(),"status":"playing",
        "questions":questions,
        "players":{host:{"score":0,"qi":0,"done":False,"wrongs":[]}}
    }
    data[f"qt_{host}_0"] = time.time()
    room_save(code, data); return data

def room_join(code, name):
    data = room_load(code)
    if data is None: return None
    if name not in data["players"]:
        data["players"][name] = {"score":0,"qi":0,"done":False,"wrongs":[]}
        data[f"qt_{name}_0"] = time.time()
        room_save(code, data)
    return data

def room_answer(code, name, correct, pts, wrong=None):
    data = room_load(code)
    if not data: return
    pl = data["players"].get(name, {"score":0,"qi":0,"done":False,"wrongs":[]})
    if correct: pl["score"] += pts
    elif wrong: pl["wrongs"].append(wrong)
    pl["qi"] += 1
    if pl["qi"] >= len(data.get("questions",[])): pl["done"] = True
    data["players"][name] = pl
    data[f"qt_{name}_{pl['qi']}"] = time.time()
    room_save(code, data)

def room_cleanup():
    for f in glob.glob(os.path.join(ROOMS_DIR,"room_*.json")):
        try:
            with open(f) as fp: d = json.load(fp)
            if time.time()-d.get("created",0) > ROOM_TTL: os.remove(f)
        except: pass

# ══════════════════════════════════════════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
DEFAULTS = {
    "screen":"home",
    "player_name":"",
    "room_code":"",
    "s_mode":None,"s_level":"🌱 Débutant","s_questions":[],"s_qi":0,
    "s_score":0,"s_wrongs":[],"s_answered":False,"s_correct":None,
    "s_timeout":False,"s_qtime":None,
    "rc_level":"🌱 Débutant",
    "new_code": None,
    "motivation_idx": random.randint(0, len(MOTIVATIONS)-1),
}
for k,v in DEFAULTS.items():
    if k not in st.session_state: st.session_state[k] = v

# ══════════════════════════════════════════════════════════════════════════════
#  DEEP LINK: ?room=CODE
# ══════════════════════════════════════════════════════════════════════════════
qp = st.query_params
if "room" in qp and st.session_state.screen == "home":
    st.session_state.room_code = qp["room"].upper()
    st.session_state.screen    = "room_join"
    st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def tl_solo():
    if st.session_state.s_qtime is None: return 99
    return max(0, LEVELS[st.session_state.s_level]["time"] - int(time.time()-st.session_state.s_qtime))

def tl_room(data, name):
    pl = data["players"].get(name,{})
    qi = pl.get("qi",0)
    qt = data.get(f"qt_{name}_{qi}")
    if qt is None: return 99
    lvl = LEVELS.get(data.get("level","🌱 Débutant"), LEVELS["🌱 Débutant"])
    return max(0, lvl["time"] - int(time.time()-qt))

def timer_html(tl, total):
    r = tl/total if total else 1
    cls = "t-green" if r>.55 else ("t-yellow" if r>.28 else "t-red")
    return f'<div style="text-align:right"><div class="timer {cls}">⏱ {tl}s</div></div>'

def notif_html(kind, pts, ans):
    if kind=="ok":    return f'<div class="notif n-ok"><h2>✅ CORRECT ! +{pts} pt{"s" if pts>1 else ""}</h2><p><strong style="color:#00ff88">{ans}</strong></p></div>'
    if kind=="wrong": return f'<div class="notif n-wrong"><h2>❌ INCORRECT</h2><p>Bonne réponse : <strong style="color:#ff8888">{ans}</strong></p></div>'
    return f'<div class="notif n-time"><h2>⌛ TEMPS ÉCOULÉ !</h2><p>La réponse était : <strong style="color:#ffaa00">{ans}</strong></p></div>'

def badge(pct):
    if pct>=90: return "🏆 LÉGENDAIRE","#00ff88"
    if pct>=70: return "⭐ EXPERT","#ffaa00"
    if pct>=50: return "👍 BIEN","#00d4ff"
    return "📚 À REVOIR","#ff4444"

def prog_html(qi, total):
    pct = int(qi/total*100) if total else 0
    return f'<div class="prog-wrap"><div class="prog-fill" style="width:{pct}%"></div></div>'

def goto(screen): st.session_state.screen = screen; st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
#  PERMANENT LEFT SIDEBAR NAVIGATION
# ══════════════════════════════════════════════════════════════════════════════
def render_sidebar():
    s = st.session_state.screen
    pname = st.session_state.player_name or "Joueur"
    with st.sidebar:
        st.markdown(f'<div class="main-title" style="font-size:1.2rem;margin-bottom:.2rem">⚡ QMP</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="p-tag">👤 {pname.upper()}</div>', unsafe_allow_html=True)

        # Room code in sidebar if in room
        if s in ("room_lobby","room_quiz","room_result","room_waiting") and st.session_state.room_code:
            code = st.session_state.room_code
            st.markdown(f'<div class="sb-room"><div class="sb-room-lbl">Salle active</div>'
                        f'<div class="sb-room-code">{code}</div>'
                        f'<div class="sb-room-lbl">🔗 ?room={code}</div></div>', unsafe_allow_html=True)

        # Score in solo quiz
        if s == "solo_quiz":
            st.markdown(f'<div class="score-box"><h3>⚡ SCORE</h3>'
                        f'<div class="big">{st.session_state.s_score}</div></div>', unsafe_allow_html=True)
            qi, total = st.session_state.s_qi, len(st.session_state.s_questions)
            st.markdown(f'<div style="color:#888;font-size:.75rem;text-align:center">Q {qi+1} / {total}</div>', unsafe_allow_html=True)
            st.markdown(prog_html(qi, total), unsafe_allow_html=True)
            lvl = LEVELS[st.session_state.s_level]
            st.markdown(f'<div style="color:{lvl["color"]};font-family:Orbitron;font-size:.68rem;'
                        f'text-align:center;letter-spacing:2px;margin:.4rem 0">{st.session_state.s_level}</div>', unsafe_allow_html=True)

        # Room scores
        if s in ("room_lobby","room_quiz","room_waiting"):
            code = st.session_state.room_code
            data = room_load(code)
            if data:
                st.markdown('<div class="hdr">👥 Scores</div>', unsafe_allow_html=True)
                total = len(data.get("questions",[]))
                for pn, pp in sorted(data["players"].items(), key=lambda x:-x[1].get("score",0)):
                    qi_p = pp.get("qi",0)
                    done = pp.get("done",False)
                    is_me = pn == st.session_state.player_name
                    status = "✅" if done else f"Q{min(qi_p+1,total)}/{total}"
                    me_cls = " me" if is_me else ""
                    me_nm  = " me" if is_me else ""
                    st.markdown(
                        f'<div class="p-row{me_cls}">'
                        f'<div class="p-dot" style="background:{PLAYER_COLORS[list(data["players"]).index(pn)%4]}"></div>'
                        f'<div class="p-name{me_nm}">{"▶ " if is_me else ""}{pn}</div>'
                        f'<div style="color:#666;font-size:.68rem;margin-right:.4rem">{status}</div>'
                        f'<div class="p-score">{pp.get("score",0)}</div>'
                        f'</div>', unsafe_allow_html=True
                    )

        st.markdown("---")

        # Navigation
        st.markdown('<div class="hdr">📍 Navigation</div>', unsafe_allow_html=True)
        if s != "home":
            if st.button("🏠 Accueil", use_container_width=True, key="nav_home"):
                goto("home")
        if s in ("solo_quiz","solo_result"):
            if st.button("🎯 Rejouer", use_container_width=True, key="nav_replay"):
                lvl = LEVELS[st.session_state.s_level]
                qs  = build_questions(st.session_state.s_mode, lvl["key"], lvl["qs"])
                if qs:
                    st.session_state.s_questions=qs; st.session_state.s_qi=0
                    st.session_state.s_score=0; st.session_state.s_wrongs=[]
                    st.session_state.s_answered=False; st.session_state.s_correct=None
                    st.session_state.s_timeout=False; st.session_state.s_qtime=None
                    goto("solo_quiz")
        if s not in ("home","solo","room_create","room_join"):
            if st.button("🎮 Changer de mode", use_container_width=True, key="nav_mode"):
                goto("solo")
        if s == "solo_quiz":
            qi_now = st.session_state.s_qi
            total_now = len(st.session_state.s_questions)
            st.markdown(f'<div style="color:#555;font-size:.72rem;text-align:center;margin-top:.4rem">'
                        f'⌛ +10s vs v2 — {qi_now}/{total_now} répondues</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  LEVEL SELECTOR (real clickable buttons)
# ══════════════════════════════════════════════════════════════════════════════
def level_selector(state_key="s_level"):
    cur = st.session_state.get(state_key, "🌱 Débutant")
    cols = st.columns(4)
    for i, (lname, lcfg) in enumerate(LEVELS.items()):
        with cols[i]:
            active = " active" if cur == lname else ""
            css    = lcfg["css"]
            # Display card
            st.markdown(
                f'<div class="{css}{active} lvl-btn">'
                f'{lname}<br>'
                f'<span style="font-size:.6rem;opacity:.7">⏱{lcfg["time"]}s · {lcfg["qs"]}Q · ×{lcfg["mult"]}</span>'
                f'</div>', unsafe_allow_html=True
            )
            # Invisible Streamlit button on top
            if st.button("Sélectionner", key=f"lvl_{state_key}_{lname}", use_container_width=True,
                         help=f"Choisir {lname}"):
                st.session_state[state_key] = lname
                st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
#  SCREEN: HOME
# ══════════════════════════════════════════════════════════════════════════════
def screen_home():
    room_cleanup()
    render_sidebar()

    # Date
    now = datetime.now()
    days_fr = ["Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi","Dimanche"]
    months_fr = ["","Janvier","Février","Mars","Avril","Mai","Juin","Juillet","Août","Septembre","Octobre","Novembre","Décembre"]
    date_str = f"{days_fr[now.weekday()]} {now.day} {months_fr[now.month]} {now.year}"
    st.markdown(f'<div class="date-banner">📅 {date_str}</div>', unsafe_allow_html=True)

    st.markdown('<div class="main-title" style="font-size:2.5rem">⚡ QUIZ MASTER PRO</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">10 Catégories · 4 Niveaux · Solo & Multijoueur</div>', unsafe_allow_html=True)

    # Motivation
    mot = MOTIVATIONS[st.session_state.motivation_idx % len(MOTIVATIONS)]
    st.markdown(f'<div class="motive-bar">{mot}</div>', unsafe_allow_html=True)

    cl, cc, cr = st.columns([1,3,1])
    with cc:
        st.markdown('<div class="card corner-deco">', unsafe_allow_html=True)
        st.markdown('<div class="hdr">👤 Qui es-tu, champion ?</div>', unsafe_allow_html=True)
        name = st.text_input("", value=st.session_state.player_name,
                             placeholder="✍️ Entre ton nom ou pseudo ici pour commencer…",
                             label_visibility="collapsed", key="home_name")
        st.session_state.player_name = name.strip()

        st.markdown('<div class="hdr">🎮 Mode de jeu</div>', unsafe_allow_html=True)
        b1, b2, b3 = st.columns(3)
        with b1:
            if st.button("🎯 Jouer en Solo", use_container_width=True, key="btn_solo"):
                if not st.session_state.player_name:
                    st.warning("⚠️ Entre ton nom d'abord !")
                else:
                    st.session_state.motivation_idx = random.randint(0,len(MOTIVATIONS)-1)
                    goto("solo")
        with b2:
            if st.button("🏠 Créer une salle", use_container_width=True, key="btn_create"):
                if not st.session_state.player_name:
                    st.warning("⚠️ Entre ton nom d'abord !")
                else:
                    st.session_state.new_code = gen_code()
                    goto("room_create")
        with b3:
            if st.button("🔗 Rejoindre", use_container_width=True, key="btn_join"):
                if not st.session_state.player_name:
                    st.warning("⚠️ Entre ton nom d'abord !")
                else:
                    goto("room_join")
        st.markdown('</div>', unsafe_allow_html=True)

    # Stats
    st.markdown("<br>", unsafe_allow_html=True)
    sc = st.columns(5)
    for i,(icon,label,mname,color) in enumerate([
        ("🔐","Finance","🔐 Sécurité Financière","#00d4ff"),
        ("🇫🇷","Français","🇫🇷 Français","#ff00ff"),
        ("🌍","Monuments","🏛️ Monuments","#ffaa00"),
        ("🎵","Musique","🎵 Musique","#ff00aa"),
        ("🧠","Culture","🌐 Culture Générale","#aa00ff"),
    ]):
        with sc[i]:
            n = csv_count(mname)
            st.markdown(
                f'<div class="stat-card">'
                f'<div style="font-size:1.6rem">{icon}</div>'
                f'<div style="color:{color};font-family:Orbitron;font-size:.58rem;letter-spacing:2px">{label.upper()}</div>'
                f'<div style="color:#fff;font-size:1.1rem;font-weight:700">{n}</div>'
                f'<div style="color:#555;font-size:.65rem">entrées</div>'
                f'</div>', unsafe_allow_html=True
            )

# ══════════════════════════════════════════════════════════════════════════════
#  SCREEN: SOLO SETUP
# ══════════════════════════════════════════════════════════════════════════════
def screen_solo():
    render_sidebar()
    st.markdown('<div class="main-title" style="font-size:1.9rem">🎯 Mode Solo</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Choisissez votre niveau et votre catégorie</div>', unsafe_allow_html=True)

    cl, cc, cr = st.columns([1,4,1])
    with cc:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="hdr">🎯 Niveau de difficulté</div>', unsafe_allow_html=True)
        level_selector("s_level")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="hdr">🎮 Choisissez votre catégorie</div>', unsafe_allow_html=True)
        mc = st.columns(2)
        for mi,(mname,mcfg) in enumerate(MODES.items()):
            with mc[mi%2]:
                c1,c2 = st.columns([3,1])
                with c1:
                    n = csv_count(mname)
                    st.markdown(
                        f'<div style="color:{mcfg["color"]};font-weight:700;font-size:.95rem">'
                        f'{mcfg["icon"]} {mname.split(" ",1)[1]}</div>'
                        f'<div style="color:#666;font-size:.7rem">{mcfg["desc"]} · {n} entrées</div>',
                        unsafe_allow_html=True
                    )
                with c2:
                    if st.button("▶", key=f"ss_{mname}", use_container_width=True):
                        lvl = LEVELS[st.session_state.s_level]
                        qs  = build_questions(mname, lvl["key"], lvl["qs"])
                        if not qs:
                            st.error("CSV vide ou introuvable.")
                        else:
                            st.session_state.s_mode=mname; st.session_state.s_questions=qs
                            st.session_state.s_qi=0; st.session_state.s_score=0
                            st.session_state.s_wrongs=[]; st.session_state.s_answered=False
                            st.session_state.s_correct=None; st.session_state.s_timeout=False
                            st.session_state.s_qtime=None; goto("solo_quiz")
        st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  SCREEN: SOLO QUIZ
# ══════════════════════════════════════════════════════════════════════════════
def screen_solo_quiz():
    render_sidebar()
    qs=st.session_state.s_questions; qi=st.session_state.s_qi; total=len(qs)
    lvl=LEVELS[st.session_state.s_level]; mode=st.session_state.s_mode; mcfg=MODES[mode]
    if qi>=total: goto("solo_result")
    q=qs[qi]
    if st.session_state.s_qtime is None and not st.session_state.s_answered:
        st.session_state.s_qtime=time.time()
    tl=tl_solo()
    if tl<=0 and not st.session_state.s_answered:
        st.session_state.s_answered=True; st.session_state.s_timeout=True; st.session_state.s_correct=False
        st.session_state.s_wrongs.append({"question":q["question"],"votre_reponse":"⌛","bonne_reponse":q["correct"]})

    # Top bar
    hc,tc = st.columns([3,1])
    with hc:
        st.markdown(f'<div class="main-title" style="font-size:1.2rem;text-align:left">{mcfg["icon"]} {mode.split(" ",1)[1]}</div>', unsafe_allow_html=True)
    with tc:
        if not st.session_state.s_answered:
            st.markdown(timer_html(tl,lvl["time"]), unsafe_allow_html=True)

    st.markdown(prog_html(qi,total), unsafe_allow_html=True)
    st.markdown(f'<div style="text-align:center;color:#00d4ff44;font-size:.7rem;letter-spacing:2px">QUESTION {qi+1} / {total}</div>', unsafe_allow_html=True)

    # Question
    st.markdown('<div class="q-card">', unsafe_allow_html=True)
    if q["prompt"]: st.markdown(f'<div class="q-prompt">{q["prompt"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="q-term">{q["question"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.s_answered:
        kind = "time" if st.session_state.s_timeout else ("ok" if st.session_state.s_correct else "wrong")
        st.markdown(notif_html(kind, lvl["mult"], q["correct"]), unsafe_allow_html=True)
        if st.button("➡️ Question suivante", use_container_width=True, key="solo_next"):
            st.session_state.s_qi+=1; st.session_state.s_answered=False
            st.session_state.s_correct=None; st.session_state.s_timeout=False
            st.session_state.s_qtime=None; st.rerun()
    else:
        c1,c2=st.columns(2)
        for idx,ch in enumerate(q["choices"]):
            with (c1 if idx%2==0 else c2):
                if st.button(f"{'ABCD'[idx]}  {ch}", key=f"sa_{qi}_{idx}", use_container_width=True):
                    ok=(ch==q["correct"])
                    st.session_state.s_answered=True; st.session_state.s_correct=ok; st.session_state.s_timeout=False
                    if ok: st.session_state.s_score+=lvl["mult"]
                    else: st.session_state.s_wrongs.append({"question":q["question"],"votre_reponse":ch,"bonne_reponse":q["correct"]})
                    st.rerun()
        if tl>0: time.sleep(1); st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
#  SCREEN: SOLO RESULT
# ══════════════════════════════════════════════════════════════════════════════
def screen_solo_result():
    render_sidebar()
    lvl=LEVELS[st.session_state.s_level]; total=len(st.session_state.s_questions)
    score=st.session_state.s_score; pct=int(score/(total*lvl["mult"])*100) if total else 0
    bdg,bc=badge(pct)

    cl,cc,cr=st.columns([1,3,1])
    with cc:
        st.markdown(f"""
        <div class="final">
          <h1>🎯 RÉSULTATS</h1>
          <div style="color:#00d4ff88;font-family:Orbitron;font-size:.75rem;letter-spacing:3px">{st.session_state.player_name.upper()}</div>
          <div class="f-score">{score} pts</div>
          <div style="font-size:1.1rem;color:#aaa;margin:.2rem">{pct}%</div>
          <div style="color:{bc};font-family:Orbitron;font-size:1.1rem;font-weight:700;text-shadow:0 0 18px {bc};margin:.7rem 0">{bdg}</div>
          <div style="color:#444;font-size:.78rem">{st.session_state.s_mode} · {st.session_state.s_level}</div>
        </div>""", unsafe_allow_html=True)

        sc1,sc2,sc3=st.columns(3)
        good=score//max(lvl["mult"],1)
        with sc1: st.markdown(f'<div class="stat-card"><div style="font-size:1.3rem">✅</div><div style="color:#00ff88;font-family:Orbitron;font-size:.6rem">BONNES</div><div style="color:#fff;font-size:1.2rem;font-weight:700">{good}</div></div>', unsafe_allow_html=True)
        with sc2: st.markdown(f'<div class="stat-card"><div style="font-size:1.3rem">📊</div><div style="color:#00d4ff;font-family:Orbitron;font-size:.6rem">TOTAL</div><div style="color:#fff;font-size:1.2rem;font-weight:700">{total}</div></div>', unsafe_allow_html=True)
        with sc3: st.markdown(f'<div class="stat-card"><div style="font-size:1.3rem">❌</div><div style="color:#ff4444;font-family:Orbitron;font-size:.6rem">ERREURS</div><div style="color:#fff;font-size:1.2rem;font-weight:700">{len(st.session_state.s_wrongs)}</div></div>', unsafe_allow_html=True)

        if st.session_state.s_wrongs:
            st.markdown('<div class="hdr">📖 Révision — Vos erreurs</div>', unsafe_allow_html=True)
            for wa in st.session_state.s_wrongs[:15]:
                st.markdown(f'<div style="background:rgba(255,68,68,.04);border:1px solid rgba(255,68,68,.15);border-radius:8px;padding:.6rem .9rem;margin:.22rem 0"><div style="color:#00d4ff;font-weight:700;font-size:.88rem">{wa["question"]}</div><div style="color:#ff8888;font-size:.75rem">Vous : {wa["votre_reponse"]}</div><div style="color:#00ff88;font-size:.75rem">✅ {wa["bonne_reponse"]}</div></div>', unsafe_allow_html=True)

        br1,br2=st.columns(2)
        with br1:
            if st.button("🔄 Rejouer", use_container_width=True, key="res_replay"):
                qs=build_questions(st.session_state.s_mode,lvl["key"],lvl["qs"])
                if qs:
                    st.session_state.s_questions=qs;st.session_state.s_qi=0
                    st.session_state.s_score=0;st.session_state.s_wrongs=[]
                    st.session_state.s_answered=False;st.session_state.s_correct=None
                    st.session_state.s_timeout=False;st.session_state.s_qtime=None
                    goto("solo_quiz")
        with br2:
            if st.button("🎮 Autre catégorie", use_container_width=True, key="res_mode"):
                goto("solo")

# ══════════════════════════════════════════════════════════════════════════════
#  SCREEN: CREATE ROOM
# ══════════════════════════════════════════════════════════════════════════════
def screen_room_create():
    render_sidebar()
    st.markdown('<div class="main-title" style="font-size:1.9rem">🏠 Créer une salle multijoueur</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Un code unique sera généré — partagez-le avec vos amis</div>', unsafe_allow_html=True)

    if st.session_state.new_code is None:
        st.session_state.new_code = gen_code()

    cl,cc,cr=st.columns([1,4,1])
    with cc:
        # Show the room code prominently BEFORE game starts
        st.markdown(f"""
        <div class="room-display">
          <div class="room-lbl">🔑 Code de votre salle</div>
          <div class="room-code-big">{st.session_state.new_code}</div>
          <div class="room-lbl" style="margin-top:.5rem">Partagez ce code par WhatsApp, SMS ou email</div>
          <div style="color:#00d4ff55;font-size:.7rem;margin-top:.4rem">🔗 URL directe : ?room={st.session_state.new_code}</div>
        </div>""", unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="hdr">🎯 Niveau</div>', unsafe_allow_html=True)
        level_selector("rc_level")

        st.markdown('<div class="hdr">🎮 Choisissez la catégorie pour démarrer</div>', unsafe_allow_html=True)
        mc=st.columns(2)
        for mi,(mname,mcfg) in enumerate(MODES.items()):
            with mc[mi%2]:
                c1,c2=st.columns([3,1])
                with c1:
                    n=csv_count(mname)
                    st.markdown(
                        f'<div style="color:{mcfg["color"]};font-weight:700;font-size:.9rem">'
                        f'{mcfg["icon"]} {mname.split(" ",1)[1]}</div>'
                        f'<div style="color:#555;font-size:.68rem">{n} entrées</div>',
                        unsafe_allow_html=True
                    )
                with c2:
                    if st.button("▶", key=f"rc_{mname}", use_container_width=True):
                        code=st.session_state.new_code
                        level=st.session_state.rc_level
                        lvl=LEVELS[level]
                        qs=build_questions(mname,lvl["key"],lvl["qs"])
                        if not qs:
                            st.error("CSV vide ou introuvable.")
                        else:
                            room_create(code,st.session_state.player_name,mname,level,qs)
                            st.session_state.room_code=code
                            st.session_state.new_code=None
                            goto("room_quiz")
        st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  SCREEN: JOIN ROOM
# ══════════════════════════════════════════════════════════════════════════════
def screen_room_join():
    render_sidebar()
    st.markdown('<div class="main-title" style="font-size:1.9rem">🔗 Rejoindre une salle</div>', unsafe_allow_html=True)

    cl,cc,cr=st.columns([1,2,1])
    with cc:
        st.markdown('<div class="card corner-deco">', unsafe_allow_html=True)
        st.markdown('<div class="hdr">🔑 Code de la salle</div>', unsafe_allow_html=True)
        code_input=st.text_input("", value=st.session_state.room_code,
                                  placeholder="Entrez le code à 6 caractères…",
                                  label_visibility="collapsed", key="join_input")
        code_input=code_input.strip().upper()
        if st.button("✅ Rejoindre la salle", use_container_width=True, key="join_btn"):
            if not code_input:
                st.warning("Entrez un code.")
            else:
                data=room_join(code_input, st.session_state.player_name)
                if data is None:
                    st.error("❌ Salle introuvable ou expirée. Vérifiez le code.")
                else:
                    st.session_state.room_code=code_input
                    goto("room_quiz")
        st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  SCREEN: ROOM QUIZ (each player plays independently)
# ══════════════════════════════════════════════════════════════════════════════
def screen_room_quiz():
    render_sidebar()
    code=st.session_state.room_code
    pname=st.session_state.player_name
    data=room_load(code)

    if data is None:
        st.error("❌ Salle introuvable ou expirée.")
        if st.button("🏠 Accueil"): goto("home")
        return

    pl=data["players"].get(pname,{"score":0,"qi":0,"done":False,"wrongs":[]})
    qi=pl.get("qi",0); qs=data.get("questions",[]); total=len(qs)
    level=data.get("level","🌱 Débutant"); lvl=LEVELS.get(level,LEVELS["🌱 Débutant"])
    mode=data.get("mode",""); mcfg=MODES.get(mode,{})
    all_done=all(p.get("done",False) for p in data["players"].values())

    # ── Done → wait or show results ──
    if pl.get("done",False) or qi>=total:
        if all_done:
            screen_room_result(data, pname, lvl, mode, level); return
        st.markdown('<div class="main-title" style="font-size:1.6rem">⏳ En attente des autres joueurs…</div>', unsafe_allow_html=True)
        still=", ".join(n for n,p in data["players"].items() if not p.get("done",False))
        st.markdown(f'<div style="text-align:center;color:#aaa;margin:1.5rem 0">Joueurs encore en jeu : <strong style="color:#00d4ff">{still}</strong></div>', unsafe_allow_html=True)
        st.markdown(prog_html(total,total), unsafe_allow_html=True)
        time.sleep(2); st.rerun(); return

    q=qs[qi]; tl=tl_room(data,pname)

    # init qtime if missing
    if f"qt_{pname}_{qi}" not in data:
        data[f"qt_{pname}_{qi}"]=time.time(); room_save(code,data); tl=lvl["time"]

    # timeout
    if tl<=0:
        room_answer(code,pname,False,0,{"question":q["question"],"votre_reponse":"⌛","bonne_reponse":q["correct"]})
        st.rerun(); return

    # Header
    hc,tc=st.columns([3,1])
    with hc:
        icon=mcfg.get("icon","🎮"); short=mode.split(" ",1)[1] if " " in mode else mode
        st.markdown(f'<div class="main-title" style="font-size:1.2rem;text-align:left">{icon} {short}</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="color:{PLAYER_COLORS[list(data["players"].keys()).index(pname)%4]};font-family:Orbitron;font-size:.75rem;letter-spacing:2px">{pname.upper()} · {pl.get("score",0)} pts</div>', unsafe_allow_html=True)
    with tc:
        st.markdown(timer_html(tl,lvl["time"]), unsafe_allow_html=True)

    st.markdown(prog_html(qi,total), unsafe_allow_html=True)
    st.markdown(f'<div style="text-align:center;color:#00d4ff44;font-size:.7rem;letter-spacing:2px">QUESTION {qi+1} / {total}</div>', unsafe_allow_html=True)

    # Question
    st.markdown('<div class="q-card">', unsafe_allow_html=True)
    prompt=mcfg.get("prompt","")
    if prompt: st.markdown(f'<div class="q-prompt">{prompt}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="q-term">{q["question"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Choices
    c1,c2=st.columns(2)
    for idx,ch in enumerate(q["choices"]):
        with (c1 if idx%2==0 else c2):
            if st.button(f"{'ABCD'[idx]}  {ch}", key=f"ra_{qi}_{idx}", use_container_width=True):
                ok=(ch==q["correct"])
                wrong=None if ok else {"question":q["question"],"votre_reponse":ch,"bonne_reponse":q["correct"]}
                room_answer(code,pname,ok,lvl["mult"],wrong)
                st.rerun()
    if tl>0: time.sleep(1); st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
#  ROOM RESULT
# ══════════════════════════════════════════════════════════════════════════════
def screen_room_result(data, pname, lvl, mode, level):
    sorted_p=sorted(data["players"].items(), key=lambda x:-x[1].get("score",0))
    total=len(data.get("questions",[]))
    medals=["🥇","🥈","🥉","4️⃣"]

    cl,cc,cr=st.columns([1,3,1])
    with cc:
        st.markdown('<div class="final">', unsafe_allow_html=True)
        st.markdown('<h1>🏆 CLASSEMENT FINAL</h1>', unsafe_allow_html=True)
        st.markdown(f'<div style="color:#555;font-size:.8rem;margin-bottom:1.2rem">{mode} · {level}</div>', unsafe_allow_html=True)
        for rank,(pn,pp) in enumerate(sorted_p):
            sc2=pp.get("score",0); pct=int(sc2/(total*lvl["mult"])*100) if total else 0
            is_me=(pn==pname); ci=list(data["players"].keys()).index(pn)%4
            st.markdown(
                f'<div style="display:flex;align-items:center;gap:.9rem;padding:.75rem 1.1rem;'
                f'background:rgba(0,0,0,.3);border:1px solid {"#00ff88" if is_me else "#222"};'
                f'border-radius:12px;margin:.35rem 0">'
                f'<div style="font-size:1.6rem">{medals[min(rank,3)]}</div>'
                f'<div style="color:{PLAYER_COLORS[ci]};font-weight:700;flex:1">{"★ " if is_me else ""}{pn}</div>'
                f'<div style="color:#666;font-size:.72rem;margin-right:.5rem">{pct}%</div>'
                f'<div style="color:#ffaa00;font-family:Orbitron;font-size:1.1rem;font-weight:900">{sc2} pts</div>'
                f'</div>', unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

        my_wrongs=data["players"].get(pname,{}).get("wrongs",[])
        if my_wrongs:
            st.markdown('<div class="hdr">📖 Votre révision</div>', unsafe_allow_html=True)
            for wa in my_wrongs[:12]:
                st.markdown(f'<div style="background:rgba(255,68,68,.04);border:1px solid rgba(255,68,68,.15);border-radius:8px;padding:.6rem .85rem;margin:.22rem 0"><div style="color:#00d4ff;font-weight:700;font-size:.85rem">{wa["question"]}</div><div style="color:#ff8888;font-size:.75rem">Vous : {wa["votre_reponse"]}</div><div style="color:#00ff88;font-size:.75rem">✅ {wa["bonne_reponse"]}</div></div>', unsafe_allow_html=True)

        if st.button("🏠 Retour au menu", use_container_width=True, key="room_home"):
            goto("home")

# ══════════════════════════════════════════════════════════════════════════════
#  ROUTER
# ══════════════════════════════════════════════════════════════════════════════
s = st.session_state.screen
if   s=="home":        screen_home()
elif s=="solo":        screen_solo()
elif s=="solo_quiz":   screen_solo_quiz()
elif s=="solo_result": screen_solo_result()
elif s=="room_create": screen_room_create()
elif s=="room_join":   screen_room_join()
elif s in ("room_lobby","room_quiz","room_result","room_waiting"): screen_room_quiz()
else:
    st.session_state.screen="home"; st.rerun()
