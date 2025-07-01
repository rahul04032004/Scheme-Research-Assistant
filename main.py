import streamlit as st
import configparser
import numpy as np
import pickle
import os
import re
import requests
from sentence_transformers import SentenceTransformer
from utils.process import extract_text_from_url, embed_and_index, save_index, load_index

# ------------------------- Config -------------------------
st.set_page_config(page_title="🛠️ Scheme Research Assistant", layout="wide")

# Load API Key
config = configparser.ConfigParser()
config.read(".config")
api_key = config["gemini"]["api_key"]

# ------------------------- Styles -------------------------
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: white;
    }
    .stApp {
        background: linear-gradient(to right, #141e30, #243b55);
        color: #f1f1f1;
    }
    .title-container {
        animation: slidein 1.5s ease-in-out;
        background: linear-gradient(to right, #8e2de2, #4a00e0);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 0 20px #00000080;
        text-align: center;
    }
    @keyframes slidein {
        0% { transform: translateY(-60px); opacity: 0; }
        100% { transform: translateY(0); opacity: 1; }
    }
    .block-container {
        padding-top: 2rem;
    }
    .stTextInput>div>input {
        background-color: #1f2937;
        color: white;
    }
    .stButton>button {
        background: linear-gradient(to right, #00c6ff, #0072ff);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------------- Title -------------------------
st.markdown('<div class="title-container"><h1>🛠️ Scheme Research Assistant</h1><p>Empowering citizens with insights on government schemes</p></div>', unsafe_allow_html=True)

# ------------------------- Session State -------------------------
if 'all_texts' not in st.session_state:
    st.session_state.all_texts = []
if 'index' not in st.session_state:
    st.session_state.index = None

# ------------------------- File Paths -------------------------
TEXT_CACHE_FILE = "text_cache.pkl"
INDEX_FILE = "faiss_store_gemini.pkl"

# ------------------------- Load Data -------------------------
if os.path.exists(TEXT_CACHE_FILE):
    try:
        with open(TEXT_CACHE_FILE, "rb") as f:
            st.session_state.all_texts = pickle.load(f)
    except Exception as e:
        st.warning(f"Error loading text cache: {e}")

if os.path.exists(INDEX_FILE):
    try:
        st.session_state.index = load_index(INDEX_FILE)
    except Exception as e:
        st.warning(f"Error loading index: {e}")

# ------------------------- Helpers -------------------------
def is_valid_url(url):
    regex = re.compile(r'^(https?|ftp):\/\/[^\s\/$.?#].[^\s]*$', re.IGNORECASE)
    return re.match(regex, url) is not None

# ------------------------- Sidebar -------------------------
with st.sidebar:
    st.header("📄 Scheme Documents")
    urls_input = st.text_area("Paste scheme URLs (one per line):", height=200)
    if st.button("Process URLs"):
        urls = [u.strip() for u in urls_input.splitlines() if u.strip()]
        invalid_urls = [u for u in urls if not is_valid_url(u)]
        if invalid_urls:
            st.error(f"Invalid URLs: {', '.join(invalid_urls)}")
        else:
            with st.spinner("Fetching and processing..."):
                new_texts = []
                for url in urls:
                    try:
                        text = extract_text_from_url(url)
                        if text:
                            new_texts.append(text)
                    except Exception as e:
                        st.warning(f"{url} failed: {str(e)}")
                if new_texts:
                    st.session_state.all_texts.extend(new_texts)
                    index, _ = embed_and_index(st.session_state.all_texts)
                    save_index(index, INDEX_FILE)
                    st.session_state.index = index
                    with open(TEXT_CACHE_FILE, "wb") as f:
                        pickle.dump(st.session_state.all_texts, f)
                    st.success(f"Indexed {len(new_texts)} new documents!")

    st.markdown("---")
    st.caption(f"📦 Documents loaded: {len(st.session_state.all_texts)}")
    if st.button("Clear Cache"):
        if os.path.exists(TEXT_CACHE_FILE):
            os.remove(TEXT_CACHE_FILE)
        if os.path.exists(INDEX_FILE):
            os.remove(INDEX_FILE)
        st.session_state.all_texts = []
        st.session_state.index = None
        st.success("Cache cleared!")

# ------------------------- Query Input -------------------------
st.subheader("🧠 Ask a Question")
query = st.text_input("Enter your question here:", placeholder="e.g. What are the benefits of PM-KISAN scheme?")
if st.button("Get Answer"):
    if not query.strip():
        st.warning("Please enter a question.")
    elif not st.session_state.all_texts or not st.session_state.index:
        st.error("Please process at least one scheme URL first.")
    else:
        try:
            model_embed = SentenceTransformer("all-MiniLM-L6-v2")
            query_vec = model_embed.encode([query])
            D, I = st.session_state.index.search(np.array(query_vec), k=1)
            if I.size == 0 or I[0][0] >= len(st.session_state.all_texts):
                st.warning("No relevant scheme found.")
            else:
                matched_text = st.session_state.all_texts[I[0][0]]
                prompt = f"""
You are a government schemes expert. Based on the content below, answer the user's question.

Content:
{matched_text}

Question: {query}

Also summarize into:
1. Benefits
2. Eligibility
3. Application Process
4. Required Documents
5. Official Website or Contact
"""
                headers = {"Content-Type": "application/json"}
                payload = {
                    "contents": [{"parts": [{"text": prompt}]}]
                }
                gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
                with st.spinner("Generating response..."):
                    r = requests.post(gemini_url, headers=headers, json=payload)
                    if r.status_code == 200:
                        answer = r.json()["candidates"][0]["content"]["parts"][0]["text"]
                        st.markdown("### 📋 Answer:")
                        st.write(answer)
                    else:
                        st.error(f"API Error: {r.status_code} - {r.text}")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
