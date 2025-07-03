# 🛠️ Scheme Research Assistant

> Empowering citizens with insights on government schemes – instantly summarized and searchable! 🇮🇳

---

## 🔍 Overview

**Scheme Research Assistant** is a web application that allows users to:
- 📎 Paste URLs of government scheme articles
- 🧠 Automatically generate detailed summaries
- ❓ Ask natural-language questions about the scheme
- ⚡ Get AI-generated answers along with benefits, eligibility, documents, and application process

Built using:
- 🌐 [Streamlit](https://streamlit.io/) – for the web interface
- 🧠 [SentenceTransformer](https://www.sbert.net/) – for text embeddings
- 🗃️ [FAISS](https://github.com/facebookresearch/faiss) – for fast semantic search
- 🤖 Gemini API – to generate intelligent responses

---

## 🚀 Features

- 📄 Input URLs of scheme articles (one per line)
- 🧵 Extracts raw text using BeautifulSoup
- 🔍 Generates sentence embeddings and indexes with FAISS
- 🧠 Allows users to ask questions about the schemes
- 📦 Caches processed documents for future use
- 🌈 Beautiful animated UI with a dark theme

---

## 📸 Preview

![App UI Preview](https://github.com/rahul04032004/Scheme-Research-Assistant/blob/main/web%20app%20screenshot.png) <!-- Replace with actual screenshot URL -->

---

## 🧑‍💻 Installation

1. **Clone this repository**
```bash
git clone https://github.com/rahul04032004/Scheme-Research-Assistant.git
cd Scheme-Research-Assistant


Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Add your Gemini API key
Create a .config file:

ini
Copy
Edit
[gemini]
api_key = your_gemini_api_key_here
Run the app

bash
Copy
Edit
streamlit run main.py
✨ Usage
Go to the sidebar

Paste one or more scheme article URLs

Click "Process URLs" to load and embed content

Ask a question like:
"What are the benefits of the PM-KISAN scheme?"

View the answer with structured summary

🗂️ Project Structure
graphql
Copy
Edit
📁 Scheme-Research-Assistant/
├── main.py                # Streamlit app
├── utils/
│   └── process.py         # Scraping and FAISS logic
├── .config                # API key (not pushed)
├── requirements.txt       # Dependencies
└── README.md              # This file
🧹 Optional Commands
🧽 Clear cached files:

bash
Copy
Edit
rm text_cache.pkl faiss_store_gemini.pkl
🙌 Acknowledgements
OpenAI + Gemini

LangChain

Streamlit

FAISS by Facebook AI

📬 Feedback & Contributions
Found a bug? Have a suggestion?
Feel free to open an issue or submit a PR! 💡

🧑‍🎓 Author
Made with ❤️ by Rahul Raj
📫 Connect on LinkedIn


