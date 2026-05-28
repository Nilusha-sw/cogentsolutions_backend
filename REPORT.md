# REPORT.md

## 1. Live Gateways

| Frontend (React SPA) | `https://cogentsolutionsassignment.netlify.app` |
| Backend API (FastAPI) | `https://cogentsolutions-backend.onrender.com` |
| Health Check | `https://cogentsolutions-backend.onrender.com/health` |
| Debug Scores | `https://cogentsolutions-backend.onrender.com/debug/scores?q=supply+chain+automation` |


## 2. Local Setup Guide

### Prerequisites
- Python 3.12
- Node.js 18+
- Git

### Clone the Repository

```bash
backend - git clone https://github.com/Nilusha-sw/cogentsolutions_backend.git
frontend - git clone https://github.com/Nilusha-sw/cogentsolutions_frontend.git
```

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data (first run only)
python -c "import nltk; nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('omw-1.4')"

# Make sure agenda.txt is in the backend/ folder, then start the server
uvicorn main:app --reload --port 8000
```

Backend runs at: `http://cogentsolutions-backend.onrender.com`

### Frontend Setup

```bash
# Open a new terminal, navigate to frontend
cd frontend

# Install dependencies
npm install

# Start the dev server
npm start
```

Frontend runs at: `http://cogentsolutionsassignment.netlify.app`

---

## 3. Content Creation Check — LinkedIn Promotional Post

> Tired of sending the same generic conference invite to every attendee? We built an AI-powered event platform for the AccelAlpha × Oracle Supply Chain Summit that reads each visitor's professional focus and career challenges, then uses a TF-IDF matching engine to pinpoint the one session most relevant to them — and drafts a personalised invitation on the spot. If you're a corporate conference planner looking to turn passive registrations into high-intent attendees, this is the system that closes the gap between a broadcast email and a conversation that converts.

---

## 4. Prompt Strategy — How Hallucination Was Prevented

Rather than relying on an LLM to decide which session fits a visitor, all matching logic was handled entirely by a classical TF-IDF cosine similarity engine built in Python. The LLM (or in the no-API version, a structured template) only receives the data that has already been retrieved and verified from `agenda.txt` — specifically the session title, speaker name, time slot, and description — and is instructed to use only those supplied fields, never invent speakers or topics, and never reference any information not explicitly passed to it. This architecture makes hallucination structurally impossible at the retrieval stage: the model is never asked "which session fits?" — it is only asked "write an email about *this* session" where *this* is a fact already extracted from the source file.

---

*Generated for: AccelAlpha × Oracle 2024 — Troubled Waters: Sailing with AI in Supply Chain*
