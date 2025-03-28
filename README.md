# 🧠 Schedule Verifier
<img src="https://media1.giphy.com/media/ieJdVmYjqq6SA09qgb/giphy_s.gif" width="400">  


---

## Overview

This application allows first-year students at Queen’s University to upload images of their class schedules and receive a structured analysis in return. It leverages cutting-edge machine learning and natural language processing technologies to convert unstructured images into verified, structured data.

## Try It Out! 🚀

Check out the live application at [https://queens-schedule-analyzer.netlify.app](https://queens-schedule-analyzer.netlify.app/)


---

## Features

- Upload one or more images of a class schedule
- Google Cloud **Document AI** extracts text using OCR
- **LangChain** and **OpenAI** analyze and structure course information
- Validates schedules and verifies computing course requirements
- Fast, responsive frontend built with **Vue.js**
- **Flask** backend orchestrates the pipeline and serves as the API layer
- **Auto-deployed on Render** with CI/CD for seamless updates

---

## Technologies Used

### Backend
- **Python**
- **Flask** – lightweight REST API
- **Google Cloud Document AI** – powerful OCR for schedule images
- **OpenAI GPT-4o** – understands and structures unstructured text
- **LangChain** – prompt orchestration and output parsing

### Frontend
- **Vue.js** – reactive single-page application for a smooth user experience
- **Vite** – lightning-fast development and production builds

### DevOps
- **Render** – automatic deployments from GitHub with environment variable support
- **Environment-based secrets** – secure management of API keys and credentials

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
