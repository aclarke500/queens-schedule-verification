# 🧠 Schedule Verifier
<img src="https://media1.giphy.com/media/ieJdVmYjqq6SA09qgb/giphy_s.gif" width="400">  


---

## 🧠 Overview

This project is your AI-powered co-pilot for navigating Queen’s CS course planning. It combines OCR, LLM reasoning, and a custom RAG pipeline to help students—especially frosh—verify their schedules, understand program requirements, and get answers to major-specific academic questions. Off-topic? The chatbot has a personality and will *gently* troll you back.

## 🚀 Try It Out

👉 [https://queens-schedule-analyzer.netlify.app](https://queens-schedule-analyzer.netlify.app/)

---

## 🔍 Features

- **Chatbot with Memory** – Built with **LangChain** + **OpenAI** for contextual multi-turn conversations
- **RAG System** – Intelligent, filtered search over parsed academic policies
- **Supabase Vector DB** – Custom cosine similarity search with major/option/specialization filters via `rpc()` functions
- **Dynamic Filter Engine** – LLM interprets user queries to apply RAG filters in real time
- **Document AI (GCP)** – OCR with Google’s Document AI for schedule parsing
- **LLM-powered Correction** – Cleans and error-corrects OCR output before validation
- **Schedule Validator** – Detects missing or incorrect courses for each major and option
- **Vue.js Frontend** – Responsive interface for chat and file upload
- **Flask API** – Manages embeddings, Supabase queries, and model calls
- **Auto-deployment on Render** – CI/CD integrated for fast iteration

## 🛠️ Technologies Used

### 🧩 Backend
- **Python** – primary backend language
- **Flask** – lightweight API server for chatbot, RAG, and OCR pipelines
- **Supabase** – free Postgres vector DB with custom RPC for similarity + filtering
- **Google Cloud Document AI** – OCR engine for extracting course text from images
- **OpenAI GPT-4o / DeepSeek** – used for reasoning, chunking, and parsing academic data
- **LangChain** – for output schema enforcement, prompt pipelines, and LLM chaining

### 🎨 Frontend
- **Vue.js** – dynamic SPA for chat, upload, and user interaction
- **Vite** – ultra-fast bundler for dev & production

### ⚙️ DevOps
- **Render** – free-tier hosting with GitHub CI/CD integration
- **.env-based secrets** – secure management of OpenAI, Supabase, and GCP keys

---

## Getting Started (Local Development)

### Prerequisites

- Python 3.10+
- Node.js 18+
- Google Cloud Service Account JSON key
- OpenAI API key

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Set environment variable for Google credentials (local)
export GOOGLE_APPLICATION_CREDENTIALS="path/to/key.json"

# Or use .env and python-dotenv if applicable
python app.py
```


### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## Deployment

- **Render Web Service (backend)**: uses Gunicorn and auto-builds with requirements.txt and Procfile
- **Netlify or Render Static Site (frontend)**: deploys from `dist/` after `npm run build`

---

## Use Case

This application was built to support incoming Queen’s University students in verifying their academic schedules. By combining OCR, LLM-based parsing, and domain-specific logic, it ensures students have clear and accurate access to their course information.

---

## License

MIT License
