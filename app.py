import streamlit as st, glob, os, json, time
from datetime import datetime
from main import run_pipeline

st.set_page_config(page_title="YGF GLOBAL INTELLIGENCE", layout="wide", page_icon="🌐")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;700&family=JetBrains+Mono:wght@400;700&display=swap');

.stApp {
    background: #05070a;
    background-image: 
        radial-gradient(circle at 20% 30%, rgba(0,255,136,0.15) 0%, transparent 40%),
        radial-gradient(circle at 80% 70%, rgba(0,102,255,0.15) 0%, transparent 40%),
        linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px);
    background-size: 100% 100%, 100% 100%, 50px 50px, 50px 50px;
}

h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; letter-spacing: -0.02em; }
p, div { font-family: 'JetBrains Mono', monospace !important; }

div[data-testid="stMetric"] {
    background: #0f1216;
    border: 1px solid #00ff88;
    border-left: 4px solid #00ff88;
    padding: 15px;
    box-shadow: 0 0 20px rgba(0,255,136,0.2);
}

.stTextInput > div > div > input {
    background: #0a0e13 !important;
    border: 1px solid #00ff88 !important;
    color: #00ff88 !important;
    font-size: 18px !important;
    border-radius: 0 !important;
}

.stButton > button {
    background: #00ff88 !important;
    color: #000 !important;
    border-radius: 0 !important;
    font-family: 'Space Grotesk' !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    letter-spacing: 2px !important;
    height: 54px !important;
    clip-path: polygon(10px 0, 100% 0, 100% calc(100% - 10px), calc(100% - 10px) 100%, 0 100%, 0 10px);
    transition: 0.2s;
}
.stButton > button:hover {
    background: #fff !important;
    box-shadow: 0 0 30px #00ff88;
    transform: translateY(-2px);
}

.news-card {
    background: #0f1216;
    border: 1px solid #1a1f29;
    border-top: 2px solid #00ff88;
    padding: 24px;
    margin-bottom: 20px;
    position: relative;
    overflow: hidden;
}
.news-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 2px;
    background: linear-gradient(90deg, #00ff88, #0066ff, transparent);
    animation: scan 3s linear infinite;
}
@keyframes scan { 0% { transform: translateX(-100%); } 100% { transform: translateX(100%); } }

.trust-HIGH { color: #00ff88; border: 1px solid #00ff88; padding: 2px 8px; font-size: 12px; }
.trust-MEDIUM { color: #ffaa00; border: 1px solid #ffaa00; padding: 2px 8px; font-size: 12px; }

.grid-bg {
    background-image: url('https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1200');
    background-size: cover;
    background-position: center;
    opacity: 0.15;
    position: fixed;
    top: 0; left: 0; width: 100%; height: 100%;
    z-index: -1;
    filter: hue-rotate(120deg) saturate(0.5);
}
</style>
<div class="grid-bg"></div>
""", unsafe_allow_html=True)

# --- HEADER ---
colH1, colH2 = st.columns([4,1])
with colH1:
    st.markdown("""
    <div style="border-left: 4px solid #00ff88; padding-left: 20px;">
        <h1 style="margin:0; font-size: 52px; color: #fff; line-height:0.9;">YGF // GLOBAL<br><span style="color:#00ff88;">INTELLIGENCE GRID</span></h1>
        <p style="color:#5a6b7c; margin-top:8px; letter-spacing:3px; font-size:12px;">MULTI-AGENT SYSTEM // COLLECTOR [ACTIVE] // VALIDATOR [ACTIVE] // WRITER [LLM: LOCAL]</p>
    </div>
    """, unsafe_allow_html=True)
with colH2:
    st.markdown(f"""
    <div style="text-align:right; color:#00ff88; border:1px solid #00ff88; padding:10px;">
        <div style="font-size:10px;">SYSTEM TIME</div>
        <div style="font-size:18px; font-weight:700;">{datetime.now().strftime('%H:%M:%S')}</div>
        <div style="font-size:10px; color:#fff;">{datetime.now().strftime('%d %b %Y')} // IST</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- COMMAND INPUT - FIXED ---
c1, c2, c3 = st.columns([6,2,2])
with c1:
    topic = st.text_input("COMMAND INPUT", placeholder="ENTER TARGET: ISRO / BUDGET / AI / GEOPOLITICS / VIRAT KOHLI", label_visibility="collapsed", key="topic_main")
with c2:
    run = st.button("EXECUTE PIPELINE >", use_container_width=True)
with c3:
    if st.button("PURGE REPORTS", use_container_width=True):
        for f in glob.glob("reports/*.json"): 
            try: os.remove(f)
            except: pass
        st.session_state.clear()
        st.rerun()

if run and topic.strip():
    with st.status(f"// INITIATING AGENTS FOR TARGET: {topic.upper()}", expanded=True) as status:
        st.write("🛰️ [AGENT-01] COLLECTOR :: SCANNING GLOBAL FEEDS")
        time.sleep(0.5)
        st.write("🛡️ [AGENT-02] VALIDATOR :: CROSS-VERIFYING + TRUST SCORING")
        time.sleep(0.5)
        st.write(f"🧠 [AGENT-03] WRITER :: LOCAL LLM :: ZERO-COST INFERENCE")
        path, data = run_pipeline(topic.strip())
        status.update(label=f"// MISSION COMPLETE :: {len(data)} INTEL PACKETS SECURED", state="complete")
        st.session_state['data'] = data
        st.session_state['path'] = path

# --- DATA VIEW ---
files = glob.glob("reports/*.json")
data = st.session_state.get('data')

if not data and files:
    try:
        with open(max(files, key=os.path.getctime), "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        data = None

if data and len(data) > 0:
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("TARGET", data[0]['topic'].upper())
    m2.metric("INTEL COUNT", f"{len(data)} PACKETS")
    m3.metric("AVG TRUST", data[0]['validation_score'])
    m4.metric("STATUS", "VERIFIED")

    st.image("https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=1400&h=400&fit=crop", caption="LIVE GLOBAL FEED MATRIX - YGF NGO")

    for i, it in enumerate(data):
        st.markdown(f"""
        <div class="news-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="color:#5a6b7c; font-size:11px;">PACKET #{i+1:02d} // {it['source_name'].upper()}</span>
                <span class="trust-{it['trust']}">{it['trust']} // {it['validation_score']}</span>
            </div>
            <h3 style="color:#fff; margin: 12px 0; font-size:22px;">{it['title']}</h3>
            <p style="color:#8a9bb0; font-size:13px;">{it['summary_2_lines']}</p>
            <p style="color:#00ff88; font-size:10px;">> {it['validation_note']} | SRC: {it['link'][:60]}</p>
        </div>
        """, unsafe_allow_html=True)
        
        t1, t2, t3, t4 = st.tabs(["LINKEDIN // PRO", "INSTAGRAM // VIRAL", "X // TWITTER", "FACEBOOK // SOCIAL"])
        with t1: st.code(it['linkedin'], language="text")
        with t2: st.code(it['instagram'], language="text")
        with t3: st.code(it['twitter'], language="text")
        with t4: st.code(it['facebook'], language="text")

else:
    st.markdown("""
    <div style="border:1px dashed #1a1f29; padding:80px 20px; text-align:center; margin-top:40px;">
        <div style="font-size:64px;">🌐</div>
        <div style="color:#fff; font-size:18px; letter-spacing:4px; margin-top:20px;">AWAITING COMMAND</div>
        <div style="color:#5a6b7c; font-size:12px; margin-top:8px;">ENTER TARGET ABOVE TO ACTIVATE INTELLIGENCE GRID</div>
    </div>
    """, unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1200&h=500&fit=crop", caption="GLOBAL NETWORK - READY")