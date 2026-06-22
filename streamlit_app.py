import os
import requests
import streamlit as st

# ── Config ────────────────────────────────────────────────────────────────────
API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Research RAG",
    page_icon="📚",
    layout="wide",
)

# ── Minimal style tweaks ──────────────────────────────────────────────────────
st.markdown("""
<style>
    .block-container { padding-top: 2rem; }
    .stChatMessage { border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Layout ────────────────────────────────────────────────────────────────────
st.title("📚 Research Paper RAG")
st.caption("Upload PDFs → ask questions → get answers grounded in your documents.")

upload_col, chat_col = st.columns([1, 1.8], gap="large")

# ── Left: Upload ──────────────────────────────────────────────────────────────
with upload_col:
    st.subheader("Ingest Documents")
    uploaded_file = st.file_uploader("Choose a PDF", type=["pdf"])

    if st.button("Index Document", use_container_width=True, type="primary"):
        if uploaded_file is None:
            st.warning("Select a PDF first.")
        else:
            with st.spinner(f"Indexing *{uploaded_file.name}*…"):
                try:
                    res = requests.post(
                        f"{API_BASE}/upload",
                        files={"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")},
                        timeout=120,
                    )
                    res.raise_for_status()
                    data = res.json()
                    st.success(f"{data['message']}  \n`{data['chunks_indexed']} chunks indexed`")
                except requests.exceptions.ConnectionError:
                    st.error("Cannot reach the API. Is FastAPI running?")
                except Exception as e:
                    st.error(f"Upload failed: {e}")

    st.divider()
    st.caption(f"**API:** `{API_BASE}`")

    # Health check
    try:
        h = requests.get(f"{API_BASE}/health", timeout=3)
        if h.ok:
            st.success("API online", icon="🟢")
        else:
            st.error("API returned an error", icon="🔴")
    except Exception:
        st.error("API offline", icon="🔴")

# ── Right: Chat ───────────────────────────────────────────────────────────────
with chat_col:
    st.subheader("Ask Questions")

    # Render history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Input
    if question := st.chat_input("Ask anything about your uploaded documents…"):
        # Show user bubble
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        # Call API
        with st.chat_message("assistant"):
            with st.spinner("Thinking…"):
                try:
                    res = requests.post(
                        f"{API_BASE}/ask",
                        json={"question": question},
                        timeout=60,
                    )
                    res.raise_for_status()
                    answer = res.json()["answer"]
                except requests.exceptions.ConnectionError:
                    answer = "⚠️ Cannot reach the API. Is FastAPI running?"
                except Exception as e:
                    answer = f"⚠️ Error: {e}"

            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

    # Clear chat button
    if st.session_state.messages:
        if st.button("Clear chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
