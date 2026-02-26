# 🧠 NeuroRead — Inclusive Digital Library & AI Reading Assistant

NeuroRead is a comprehensive, full-stack web application designed to make reading digital documents accessible, highly customizable, and cognitively supportive for everyone. It specifically targets users with varying reading needs, including Dyslexia, ADHD, and Visual Impairments, by utilizing an Agentic AI engine and deeply integrated accessibility tools.

---

## ✨ Key Features

### 🛠️ Core Library & Reading
*   **Custom Document Uploads:** Upload and parse `.pdf` documents and plain text files seamlessly.
*   **Cloud Progress Sync:** Automatically saves and syncs your exact reading progress across sessions.
*   **Advanced Annotation System:** Multi-color highlighting and a built-in interactive Notes manager with quote tracking.
*   **Secure Authentication:** JWT-based login, registration, and session management.

### 🤖 Agentic AI Integrations (HuggingFace API)
*   **Proactive Complexity Detection:** The system silently analyzes the text on the page. If it detects highly complex vocabulary or overly long sentences, an intelligent banner proactively offers assistance.
*   **1-Click Simplification:** Utilizes NLP models (`sshleifer/distilbart-cnn-12-6`) to summarize and simplify difficult paragraphs instantly.
*   **Smart Structuring:** Converts dense walls of text into easily readable bullet points.
*   **In-Context Dictionary:** Double-click any complex word while reading to get an AI-generated definition and contextual explanation via an interactive tooltip overlay.
*   **Multi-lingual Translation:** Instant translation of text into regional languages (Malayalam, Kannada, Telugu, Hindi) using `deep-translator`.

### ♿ Cognitive Profiling & Accessibility (Smart Presets)
*   **Dyslexia Profile:** Automatically overrides text with the highly legible `Atkinson Hyperlegible` font, increases letter spacing, and applies a warm Sage background to reduce glare.
*   **ADHD / Focus Profile:** Automatically injects the `DM Sans` font, minimizes UI distractions, and auto-enables Focus Mode.
*   **Visual Impairment Profile:** Enforces high-contrast pure black and white styling, and massively scales up the base font sizes.
*   **Focus Mode:** Dims all text on the screen except the specific line you are currently reading (navigable via arrow keys).
*   **Reading Ruler:** A dynamic, follow-my-cursor semi-transparent ruler to help guide the eyes horizontally.
*   **Read Aloud (TTS):** Built-in Text-To-Speech engine that reads the text aloud and highlights individual words synchronously as they are spoken.

### 🎨 Modern UI/UX
*   **LinkedIn-Style Profile Dashboard:** A modern, multi-column dynamic Dashboard featuring a cover photo banner, circular offset avatars, and live-preview settings chips.
*   **Glassmorphism & Micro-animations:** Premium aesthetic using frosted glass UI layers, staggered element loading, skeleton loaders, and interactive hover states.

---

## 💻 Tech Stack

### Frontend
*   **Core:** HTML5, Modern CSS3 (CSS Grid, Flexbox, Variable cascade), Vanilla JavaScript (ES6+).
*   **Styling:** Custom CSS, no heavy frameworks required. Pure CSS Glassmorphism.
*   **Parsers / Utilities:** `PDF.js` (for rendering client-side PDFs), `FontAwesome` (iconography).

### Backend
*   **Framework:** Django & Django REST Framework (DRF)
*   **Database:** SQLite3
*   **Authentication:** `djangorestframework-simplejwt`
*   **AI Models:** HuggingFace Inference API (Server-side proxying to protect API keys)
*   **Translation:** `deep-translator` library

---

## 🚀 Setup Instructions

### 1. Backend Setup
1. Open a terminal in the project root directory.
2. Create a virtual environment: `python -m venv .venv`
3. Activate it:
   - Windows: `.venv\Scripts\activate`
   - Mac/Linux: `source .venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt` *(Make sure Django, djangorestframework, djangorestframework-simplejwt, requests, and deep-translator are installed)*.
5. Apply database migrations: `python manage.py makemigrations` and `python manage.py migrate`
6. Start the Django server: `python manage.py runserver`

*(Server runs on `http://127.0.0.1:8000`)*

### 2. Frontend Setup
1. Open a **new** terminal window in the `frontend/` folder.
2. Start a local HTTP server: `python -m http.server 5500`
3. Open your browser and navigate to: `http://127.0.0.1:5500/login.html`

### 3. Environment Variables
To enable the Agentic AI features, create a `.env` file in the same directory as `settings.py` (inner `Zsquad/` folder) and add your HuggingFace API key:
```env
HF_API_KEY=hf_your_api_key_here
```

---

## 📁 Project Architecture

- `/frontend` - Contains all HTML, CSS, and JS logic. Designed to be completely decoupled from Django templates to emulate a true headless SPA architecture.
- `/library` - Django app handling file uploads, user document hosting, and reading progress synchronization.
- `/user_preferences` - Django app managing the Cognitive Profiles and dynamic generation of Smart CSS presets.
- `/ai_features` - Django app proxying requests safely to HuggingFace, managing complexity detection workflows and definitions.
- `/translator` - Django app dedicated to handling external ML translation requests.
- `/accounts` - Django app managing custom User models and JWT token generation.
