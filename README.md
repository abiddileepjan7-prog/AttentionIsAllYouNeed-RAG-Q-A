# 📄 RAG Question Answering System (Transformer Paper)

A **Retrieval-Augmented Generation (RAG)** application that allows users to ask questions about a PDF (specifically *“Attention Is All You Need”*) through a web interface and get accurate, context-based answers using an LLM.

---

## 🚀 Features

* 🔍 Semantic search using embeddings
* 🤖 LLM-powered answers (via Groq API)
* 📄 PDF-based knowledge (Transformer paper)
* 🌐 FastAPI backend
* 🖥️ Simple frontend (HTML + JS)
* ⚡ Lazy loading for performance
* 🧠 Context-aware responses (reduces hallucination)

---

## 🧠 How it Works

1. Load PDF document
2. Split into smaller chunks
3. Convert text into embeddings
4. Store in vector database (Chroma)
5. On user query:

   * Retrieve most relevant chunks
   * Send context + question to LLM
   * Return generated answer

---

## 🏗️ Tech Stack

* Python
* LangChain
* FastAPI
* ChromaDB
* HuggingFace Embeddings (`all-MiniLM-L6-v2`)
* Groq LLM (`llama-3.3-70b-versatile`)

---

## 📂 Project Structure

```
project/
│
├── rag.py                # Backend (FastAPI + RAG pipeline)
├── .env                 # API key (ignored in git)
├── .gitignore
├── requirements.txt
│
├── static/              # CSS / JS files
├── templates/
│   └── index.html       # Frontend UI
│
└── NIPS-2017-attention-is-all-you-need-Paper.pdf
```

---

## ⚙️ Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

---

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

---

### 4. Add API key

Create a `.env` file:

```
GROQ_API_KEY=your_api_key_here
```

---

### 5. Run the app

```bash
uvicorn rag:app --reload
```

---

### 6. Open in browser

```
http://127.0.0.1:8000
```

---

## 📡 API Endpoints

### 🔹 Ask Question

```
POST /ask
```

**Request:**

```json
{
  "question": "What optimizer is used?"
}
```

**Response:**

```json
{
  "answer": "The paper uses the Adam optimizer..."
}
```

---

### 🔹 Health Check

```
GET /health
```

---

## 🔐 Security

* API keys are stored in `.env`
* `.env` is excluded via `.gitignore`

---

## ⚠️ Notes

* First run may take time (downloads embedding model)
* Requires internet for initial setup
* Ensure correct PDF path

---

## 📌 Future Improvements

* Chat-style UI (like ChatGPT)
* Persistent vector database
* Multi-document support
* Source citation in answers
* Authentication & deployment

---

## 🙌 Acknowledgements

* Transformer paper: *“Attention Is All You Need”*
* LangChain ecosystem
* Groq for fast LLM inference

---

## 📧 Contact

Feel free to reach out for collaboration or improvements!

---
