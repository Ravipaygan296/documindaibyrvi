import streamlit as st
from rag_engine import RAGEngine

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DocuMind AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --bg: #08080f;
    --card: #12121a;
    --card2: #1a1a25;
    --accent: #7c6af7;
    --accent2: #f06292;
    --glow: rgba(124,106,247,0.15);
    --border: rgba(124,106,247,0.2);
    --text: #f0eeff;
    --muted: #7a7a9a;
    --green: #4caf87;
}

* { box-sizing: border-box; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main .block-container {
    background: var(--bg) !important;
    font-family: 'DM Sans', sans-serif;
    color: var(--text);
    padding-top: 0 !important;
}

/* Hide sidebar completely */
[data-testid="stSidebar"],
[data-testid="collapsedControl"] { display: none !important; }

/* Remove default streamlit padding */
.main .block-container {
    max-width: 1100px !important;
    padding: 2rem 2rem 4rem !important;
    margin: 0 auto !important;
}

#MainMenu, footer, header { visibility: hidden; }

h1,h2,h3 { font-family: 'Syne', sans-serif !important; color: var(--text) !important; }

/* ── Hero ── */
.hero { text-align: center; padding: 3rem 1rem 2rem; }
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 3.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #7c6af7, #f06292);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -1.5px;
    margin-bottom: 0.5rem;
}
.hero-sub { color: var(--muted); font-size: 1rem; font-weight: 300; margin-bottom: 0.3rem; }
.badge {
    display: inline-block;
    background: rgba(76,175,135,0.12);
    border: 1px solid rgba(76,175,135,0.3);
    border-radius: 20px;
    padding: 0.25rem 0.9rem;
    font-size: 0.75rem;
    color: #4caf87;
    letter-spacing: 0.5px;
    margin-top: 0.5rem;
}

.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: var(--muted);
    margin-bottom: 0.8rem;
}

/* ── Feature cards ── */
.feat-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.4rem;
    height: 100%;
    transition: all 0.3s;
}
.feat-card:hover {
    border-color: var(--accent);
    box-shadow: 0 0 24px var(--glow);
    transform: translateY(-2px);
}
.feat-icon { font-size: 1.6rem; margin-bottom: 0.6rem; }
.feat-title { font-family: 'Syne',sans-serif; font-weight: 700; font-size: 0.95rem; margin-bottom: 0.3rem; color: var(--text); }
.feat-desc { color: var(--muted); font-size: 0.8rem; line-height: 1.5; }

/* ── Stat cards ── */
.stat-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
}
.stat-num { font-family: 'Syne',sans-serif; font-size: 2rem; font-weight: 700; color: var(--accent); }
.stat-lbl { font-size: 0.7rem; color: var(--muted); text-transform: uppercase; letter-spacing: 1px; }

/* ── Chat bubbles ── */
.chat-user {
    background: rgba(124,106,247,0.1);
    border: 1px solid rgba(124,106,247,0.25);
    border-radius: 14px 14px 2px 14px;
    padding: 0.9rem 1.2rem;
    margin: 0.6rem 0 0.6rem auto;
    max-width: 78%;
    font-size: 0.92rem;
    color: var(--text);
}
.chat-ai {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 2px 14px 14px 14px;
    padding: 0.9rem 1.2rem;
    margin: 0.6rem 0;
    max-width: 88%;
    font-size: 0.92rem;
    color: var(--text);
    line-height: 1.7;
}

/* ── Source box ── */
.source-box {
    background: var(--card2);
    border: 1px solid rgba(240,98,146,0.2);
    border-left: 3px solid var(--accent2);
    border-radius: 10px;
    padding: 1rem 1.4rem;
    margin: 0.5rem 0;
    font-size: 0.83rem;
    color: #d0d0e8;
    line-height: 1.6;
}
.source-hdr {
    font-family: 'Syne', sans-serif;
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: var(--accent2);
    margin-bottom: 0.5rem;
}

.settings-row {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1rem 1.5rem;
}

.divider { border: none; border-top: 1px solid var(--border); margin: 1.5rem 0; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #7c6af7, #9b59f7) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.3px !important;
    transition: all 0.25s !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 20px rgba(124,106,247,0.35) !important;
}

.stTextInput > div > div > input {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    padding: 0.7rem 1rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px var(--glow) !important;
}

[data-testid="stFileUploaderDropzone"] {
    background: var(--card2) !important;
    border: 1.5px dashed var(--border) !important;
    border-radius: 12px !important;
}

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--accent); border-radius: 4px; }

.banner-ok {
    background: rgba(76,175,135,0.1);
    border: 1px solid rgba(76,175,135,0.3);
    border-radius: 10px;
    padding: 0.7rem 1.2rem;
    color: #4caf87;
    font-size: 0.85rem;
}
.banner-info {
    background: rgba(124,106,247,0.08);
    border: 1px solid rgba(124,106,247,0.2);
    border-radius: 10px;
    padding: 0.7rem 1.2rem;
    color: #a89cf7;
    font-size: 0.85rem;
}
</style>
""", unsafe_allow_html=True)

# ─── Session State ────────────────────────────────────────────────────────────
for k, v in {
    "rag_engine": None,
    "chat_history": [],
    "docs_processed": False,
    "doc_stats": {}
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─── API Config ───────────────────────────────────────────────────────────────
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
PROVIDER     = "groq"
MODEL_NAME   = "llama-3.3-70b-versatile"

# ═══════════════════════════════════════════════════════════════════
# HERO
# ═══════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
    <div class="hero-title">🧠 DocuMind AI</div>
    <div class="hero-sub">Upload documents · Ask questions · Get cited answers</div>
    <div class="badge">✓ Powered by LLaMA 3.3 · No setup needed</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# STEP 1 — UPLOAD + SETTINGS
# ═══════════════════════════════════════════════════════════════════
st.markdown('<p class="section-label">📁 Step 1 — Upload Your PDFs</p>', unsafe_allow_html=True)

upload_col, settings_col = st.columns([3, 2])

with upload_col:
    uploaded_files = st.file_uploader(
        "Upload PDFs",
        type=["pdf"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

with settings_col:
    st.markdown('<div class="settings-row">', unsafe_allow_html=True)
    st.markdown('<p class="section-label">⚙ Settings</p>', unsafe_allow_html=True)
    chunk_size = st.slider("Chunk Size", 300, 1000, 500, 50,
                           help="Smaller = more precise retrieval. Larger = more context per chunk.")
    top_k = st.slider("Sources to Retrieve", 2, 6, 3,
                      help="How many document chunks to use per question.")
    st.markdown('</div>', unsafe_allow_html=True)

if uploaded_files:
    if st.button("⚡  Process Documents  →", use_container_width=True):
        with st.spinner("🔄 Parsing PDFs, creating embeddings and building FAISS index..."):
            try:
                engine = RAGEngine(
                    api_key=GROQ_API_KEY,
                    provider=PROVIDER,
                    model_name=MODEL_NAME,
                    chunk_size=chunk_size,
                    top_k=top_k
                )
                stats = engine.process_documents(uploaded_files)
                st.session_state.rag_engine = engine
                st.session_state.docs_processed = True
                st.session_state.doc_stats = stats
                st.session_state.chat_history = []
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
else:
    st.markdown(
        '<div class="banner-info">👆 Upload one or more PDF files above, then click ⚡ Process Documents</div>',
        unsafe_allow_html=True
    )

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# STEP 2 — CHAT OR WELCOME
# ═══════════════════════════════════════════════════════════════════
if not st.session_state.docs_processed:

    st.markdown('<p class="section-label">✨ What DocuMind Can Do</p>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    for col, (icon, title, desc) in zip([c1,c2,c3], [
        ("🔍", "Semantic Search",    "Finds relevant passages using vector embeddings — understands meaning, not just keywords"),
        ("📌", "Source Citations",   "Every answer cites the exact page and document it came from — fully transparent"),
        ("⚡", "Zero Hallucination", "LLM only reads retrieved context — it cannot make things up from training data"),
    ]):
        with col:
            st.markdown(f"""
            <div class="feat-card">
                <div class="feat-icon">{icon}</div>
                <div class="feat-title">{title}</div>
                <div class="feat-desc">{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;padding:2.5rem 0 1rem;color:#7a7a9a;font-size:0.88rem;">
        Upload a PDF above and click <strong style="color:#a89cf7">⚡ Process Documents</strong> to begin
    </div>""", unsafe_allow_html=True)

else:
    # Stats
    stats = st.session_state.doc_stats
    s1,s2,s3,s4 = st.columns(4)
    for col, (val, lbl) in zip([s1,s2,s3,s4], [
        (stats.get("num_docs",0),   "Documents"),
        (stats.get("num_chunks",0), "Chunks"),
        (stats.get("total_pages",0),"Pages"),
        (len(st.session_state.chat_history), "Questions Asked"),
    ]):
        with col:
            st.markdown(
                f'<div class="stat-card"><div class="stat-num">{val}</div><div class="stat-lbl">{lbl}</div></div>',
                unsafe_allow_html=True)

    st.markdown("")
    st.markdown('<div class="banner-ok">✓ Documents indexed! Ask anything below.</div>',
                unsafe_allow_html=True)
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Conversation
    if st.session_state.chat_history:
        st.markdown('<p class="section-label">💬 Conversation</p>', unsafe_allow_html=True)
        for item in st.session_state.chat_history:
            st.markdown(f'<div class="chat-user">🙋 {item["question"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="chat-ai">🧠 {item["answer"]}</div>', unsafe_allow_html=True)
            if item.get("sources"):
                with st.expander(f"📌 View {len(item['sources'])} source(s)", expanded=False):
                    for i, src in enumerate(item["sources"]):
                        st.markdown(f"""
                        <div class="source-box">
                            <div class="source-hdr">Source {i+1} · {src.get('file','Document')} · Page {src.get('page','?')}</div>
                            {src.get('content','')}
                        </div>""", unsafe_allow_html=True)
        st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Ask
    st.markdown('<p class="section-label">🔍 Step 2 — Ask a Question</p>', unsafe_allow_html=True)

    suggestions = [
        "Summarize the key findings",
        "What are the main conclusions?",
        "List the important data points",
        "What methodology was used?",
    ]
    s_cols = st.columns(4)
    clicked = None
    for col, sug in zip(s_cols, suggestions):
        with col:
            if st.button(sug, use_container_width=True, key=f"s_{sug}"):
                clicked = sug

    query = st.text_input(
        "Question",
        placeholder="Type your question here or click a suggestion above...",
        label_visibility="collapsed",
        key="query_input"
    )

    final_query = clicked or query

    a_col, c_col, e_col = st.columns([5, 1, 1])
    with a_col:
        ask_btn = st.button("Ask DocuMind →", use_container_width=True)
    with c_col:
        if st.button("🗑 Clear", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    with e_col:
        if st.session_state.chat_history:
            txt = ""
            for item in st.session_state.chat_history:
                txt += f"Q: {item['question']}\n\nA: {item['answer']}\n\n"
                for i, src in enumerate(item.get("sources",[])):
                    txt += f"Source {i+1}: {src.get('content','')}\n"
                txt += "\n" + "─"*60 + "\n\n"
            st.download_button("⬇ Export", txt, "chat_export.txt", "text/plain",
                               use_container_width=True)

    if (ask_btn or clicked) and final_query:
        with st.spinner("🔍 Searching documents and generating answer..."):
            try:
                result = st.session_state.rag_engine.query(final_query)
                st.session_state.chat_history.append({
                    "question": final_query,
                    "answer":   result["answer"],
                    "sources":  result["sources"]
                })
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")



