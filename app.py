import streamlit as st
import os
import time
from pathlib import Path
from rag_engine import RAGEngine

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DocuMind AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

:root {
    --bg-primary: #0a0a0f;
    --bg-secondary: #111118;
    --bg-card: #16161f;
    --accent: #7c6af7;
    --accent-2: #f06292;
    --accent-glow: rgba(124, 106, 247, 0.15);
    --text-primary: #f0eeff;
    --text-muted: #7a7a9a;
    --border: rgba(124, 106, 247, 0.2);
    --success: #4caf87;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg-primary) !important;
    font-family: 'DM Sans', sans-serif;
    color: var(--text-primary);
}

[data-testid="stSidebar"] {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] > div {
    padding-top: 2rem;
}

h1, h2, h3 {
    font-family: 'Syne', sans-serif !important;
    color: var(--text-primary) !important;
}

.main-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #7c6af7 0%, #f06292 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -1px;
    line-height: 1.1;
    margin-bottom: 0.2rem;
}

.subtitle {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.95rem;
    color: var(--text-muted);
    font-weight: 300;
    letter-spacing: 0.5px;
}

.stat-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    text-align: center;
    transition: all 0.3s ease;
}

.stat-card:hover {
    border-color: var(--accent);
    box-shadow: 0 0 20px var(--accent-glow);
}

.stat-number {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: var(--accent);
}

.stat-label {
    font-size: 0.75rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 0.2rem;
}

.answer-box {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent);
    border-radius: 12px;
    padding: 1.5rem 2rem;
    margin: 1rem 0;
    position: relative;
}

.answer-box::before {
    content: '🧠';
    position: absolute;
    top: -12px;
    left: 16px;
    font-size: 1.2rem;
    background: var(--bg-primary);
    padding: 0 6px;
}

.source-chip {
    display: inline-block;
    background: rgba(124, 106, 247, 0.12);
    border: 1px solid rgba(124, 106, 247, 0.3);
    border-radius: 20px;
    padding: 0.3rem 0.8rem;
    font-size: 0.78rem;
    color: #a89cf7;
    margin: 0.2rem;
    font-family: 'DM Sans', sans-serif;
}

.source-box {
    background: var(--bg-card);
    border: 1px solid rgba(240, 98, 146, 0.2);
    border-left: 3px solid var(--accent-2);
    border-radius: 10px;
    padding: 1rem 1.5rem;
    margin: 0.5rem 0;
    font-size: 0.85rem;
    color: #d0d0e8;
    line-height: 1.6;
}

.source-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: var(--accent-2);
    margin-bottom: 0.5rem;
}

.chat-user {
    background: rgba(124, 106, 247, 0.1);
    border: 1px solid rgba(124, 106, 247, 0.25);
    border-radius: 12px 12px 2px 12px;
    padding: 0.8rem 1.2rem;
    margin: 0.5rem 0;
    font-size: 0.9rem;
    max-width: 80%;
    margin-left: auto;
    color: var(--text-primary);
}

.chat-ai {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 2px 12px 12px 12px;
    padding: 0.8rem 1.2rem;
    margin: 0.5rem 0;
    font-size: 0.9rem;
    max-width: 85%;
    color: var(--text-primary);
    line-height: 1.6;
}

.upload-zone {
    border: 2px dashed var(--border);
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    transition: all 0.3s ease;
    background: var(--bg-card);
}

.upload-zone:hover {
    border-color: var(--accent);
    background: var(--accent-glow);
}

.stButton > button {
    background: linear-gradient(135deg, #7c6af7, #9b59f7) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    padding: 0.6rem 1.5rem !important;
    transition: all 0.3s ease !important;
    letter-spacing: 0.3px !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(124, 106, 247, 0.35) !important;
}

.stTextInput > div > div > input {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    font-family: 'DM Sans', sans-serif !important;
    padding: 0.7rem 1rem !important;
}

.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px var(--accent-glow) !important;
}

.stSelectbox > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
}

.stFileUploader {
    background: var(--bg-card) !important;
    border: 1px dashed var(--border) !important;
    border-radius: 12px !important;
    padding: 1rem !important;
}

.stFileUploader label {
    color: var(--text-muted) !important;
}

[data-testid="stFileUploaderDropzone"] {
    background: var(--bg-card) !important;
    border: 1.5px dashed var(--border) !important;
    border-radius: 12px !important;
}

.success-banner {
    background: rgba(76, 175, 135, 0.1);
    border: 1px solid rgba(76, 175, 135, 0.3);
    border-radius: 10px;
    padding: 0.8rem 1.2rem;
    color: #4caf87;
    font-size: 0.88rem;
    margin: 0.5rem 0;
}

.processing-banner {
    background: rgba(124, 106, 247, 0.08);
    border: 1px solid rgba(124, 106, 247, 0.2);
    border-radius: 10px;
    padding: 0.8rem 1.2rem;
    color: #a89cf7;
    font-size: 0.88rem;
}

.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: var(--text-muted);
    margin-bottom: 0.8rem;
}

.divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 1.5rem 0;
}

.history-item {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.6rem 1rem;
    margin: 0.3rem 0;
    cursor: pointer;
    font-size: 0.82rem;
    color: var(--text-muted);
    transition: all 0.2s;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.history-item:hover {
    border-color: var(--accent);
    color: var(--text-primary);
}

/* Scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--accent); border-radius: 4px; }

/* Remove streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ─── Session State Init ──────────────────────────────────────────────────────
if "rag_engine" not in st.session_state:
    st.session_state.rag_engine = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "docs_processed" not in st.session_state:
    st.session_state.docs_processed = False
if "doc_stats" not in st.session_state:
    st.session_state.doc_stats = {}
if "api_key_set" not in st.session_state:
    st.session_state.api_key_set = True  # Always set — key is hardcoded

# ─── API Config (Loaded from Streamlit Secrets — never hardcode keys!) ───────
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
PROVIDER     = "groq"
MODEL_NAME   = "llama-3.3-70b-versatile"

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p class="main-title" style="font-size:1.6rem;">DocuMind<br><span style="color:#f06292">AI</span></p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">RAG Document Intelligence</p>', unsafe_allow_html=True)
    st.markdown('<div class="success-banner">✓ Powered by LLaMA 3 · Ready to use</div>', unsafe_allow_html=True)
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Upload
    st.markdown('<p class="section-label">📁 Documents</p>', unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        "Upload PDFs",
        type=["pdf"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

    chunk_size = st.slider("Chunk Size", 300, 1000, 500, 50, help="Size of text chunks for retrieval")
    top_k = st.slider("Sources to Retrieve", 2, 6, 3, help="Number of source chunks to retrieve per query")

    if uploaded_files:
        if st.button("⚡ Process Documents", use_container_width=True):
            with st.spinner(""):
                st.markdown('<div class="processing-banner">🔄 Chunking & embedding documents...</div>', unsafe_allow_html=True)
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
                    st.error(f"Error: {str(e)}")

    # Doc Stats
    if st.session_state.docs_processed:
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown('<p class="section-label">📊 Index Stats</p>', unsafe_allow_html=True)
        stats = st.session_state.doc_stats
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'<div class="stat-card"><div class="stat-number">{stats.get("num_docs", 0)}</div><div class="stat-label">Docs</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="stat-card"><div class="stat-number">{stats.get("num_chunks", 0)}</div><div class="stat-label">Chunks</div></div>', unsafe_allow_html=True)

    # Chat History
    if st.session_state.chat_history:
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown('<p class="section-label">💬 History</p>', unsafe_allow_html=True)
        for i, item in enumerate(st.session_state.chat_history[-5:]):
            q = item["question"][:45] + "..." if len(item["question"]) > 45 else item["question"]
            st.markdown(f'<div class="history-item">Q: {q}</div>', unsafe_allow_html=True)
        if st.button("🗑 Clear History", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

# ─── Main Content ─────────────────────────────────────────────────────────────
col_title, col_badge = st.columns([3, 1])
with col_title:
    st.markdown('<h1 class="main-title">DocuMind AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Upload documents · Ask questions · Get cited answers</p>', unsafe_allow_html=True)

st.markdown("")

# ─── Welcome / Empty State ───────────────────────────────────────────────────
if not st.session_state.docs_processed:
    st.markdown("""
    <div style="text-align:center; padding: 4rem 2rem;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🧠</div>
        <h2 style="font-family: 'Syne', sans-serif; color: #f0eeff; font-size: 1.8rem; margin-bottom: 0.5rem;">
            Intelligent Document Analysis
        </h2>
        <p style="color: #7a7a9a; font-size: 0.95rem; max-width: 500px; margin: 0 auto 2rem;">
            Simply upload your PDFs in the sidebar and start asking questions — no setup needed, powered by LLaMA 3.
        </p>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(3)
    features = [
        ("🔍", "Semantic Search", "Finds relevant passages using vector embeddings, not just keywords"),
        ("📌", "Source Citations", "Every answer links back to exact passages in your documents"),
        ("⚡", "Free LLMs", "Works with Groq (LLaMA) and Gemini — both free tier supported"),
    ]
    for col, (icon, title, desc) in zip(cols, features):
        with col:
            st.markdown(f"""
            <div class="stat-card" style="text-align:left; padding: 1.5rem;">
                <div style="font-size:1.8rem; margin-bottom:0.8rem;">{icon}</div>
                <div style="font-family:'Syne',sans-serif; font-weight:600; margin-bottom:0.4rem; color:#f0eeff;">{title}</div>
                <div style="color:#7a7a9a; font-size:0.82rem; line-height:1.5;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

# ─── Chat Interface ───────────────────────────────────────────────────────────
else:
    # Stats row
    stats = st.session_state.doc_stats
    c1, c2, c3, c4 = st.columns(4)
    metrics = [
        (stats.get("num_docs", 0), "Documents"),
        (stats.get("num_chunks", 0), "Chunks"),
        (stats.get("total_pages", 0), "Pages"),
        (len(st.session_state.chat_history), "Questions Asked"),
    ]
    for col, (val, label) in zip([c1, c2, c3, c4], metrics):
        with col:
            st.markdown(f'<div class="stat-card"><div class="stat-number">{val}</div><div class="stat-label">{label}</div></div>', unsafe_allow_html=True)

    st.markdown("")

    # Chat history display
    if st.session_state.chat_history:
        st.markdown('<p class="section-label">💬 Conversation</p>', unsafe_allow_html=True)
        for item in st.session_state.chat_history:
            st.markdown(f'<div class="chat-user">🙋 {item["question"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="chat-ai">🧠 {item["answer"]}</div>', unsafe_allow_html=True)
            
            if item.get("sources"):
                with st.expander(f"📌 View {len(item['sources'])} Source(s)", expanded=False):
                    for idx, src in enumerate(item["sources"]):
                        st.markdown(f"""
                        <div class="source-box">
                            <div class="source-title">Source {idx+1} · {src.get('file', 'Document')} · Page {src.get('page', '?')}</div>
                            {src.get('content', '')}
                        </div>
                        """, unsafe_allow_html=True)

        st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Query Input
    st.markdown('<p class="section-label">🔍 Ask a Question</p>', unsafe_allow_html=True)
    
    # Suggested questions
    doc_names = st.session_state.doc_stats.get("doc_names", [])
    suggestions = [
        "Summarize the key findings",
        "What are the main conclusions?",
        "List the important data points",
        "What methodology was used?",
    ]
    
    cols = st.columns(len(suggestions))
    clicked_suggestion = None
    for col, sug in zip(cols, suggestions):
        with col:
            if st.button(sug, use_container_width=True, key=f"sug_{sug}"):
                clicked_suggestion = sug

    query = st.text_input(
        "Your question",
        placeholder="Ask anything about your documents...",
        label_visibility="collapsed",
        key="query_input"
    )

    final_query = clicked_suggestion or query

    col_ask, col_export = st.columns([4, 1])
    with col_ask:
        ask_clicked = st.button("Ask DocuMind →", use_container_width=True)
    with col_export:
        if st.session_state.chat_history:
            if st.button("Export Chat", use_container_width=True):
                export_text = ""
                for item in st.session_state.chat_history:
                    export_text += f"Q: {item['question']}\n\nA: {item['answer']}\n\n"
                    for i, src in enumerate(item.get("sources", [])):
                        export_text += f"Source {i+1}: {src.get('content','')}\n"
                    export_text += "\n" + "─"*60 + "\n\n"
                st.download_button("⬇ Download", export_text, "chat_export.txt", "text/plain")

    if (ask_clicked or clicked_suggestion) and final_query:
        with st.spinner("Searching documents and generating answer..."):
            try:
                result = st.session_state.rag_engine.query(final_query)
                st.session_state.chat_history.append({
                    "question": final_query,
                    "answer": result["answer"],
                    "sources": result["sources"]
                })
                st.rerun()
            except Exception as e:
                st.error(f"Error generating answer: {str(e)}")

