# NEU Intelligent Student Hub





A comprehensive, AI-integrated academic management portal tailored for students at the National Economics University (NEU). This platform streamlines academic workflows, financial tracking, and digital resource discovery through a modern, user-centric interface.

## Key Features

### Next-Gen Dashboard

* Digital Student ID: Secure, personalized identification card with QR integration.

* Real-time Analytics: Instant visualization of Cumulative GPA, Earned Credits, and Tuition status.

* Dynamic Scheduling: Automated weekly timetable synchronized with enrollment data.

### Digital Library (Personalized)

* Heuristic Recommendations: Automatically suggests textbooks and resources based on the user's current semester enrollment.

* Immersive UI: A modern "Manga Portal" aesthetic featuring horizontal scrollers, trending ranks, and minimalist cover art for missing assets.

* Rich Metadata: Interactive modals providing book abstracts, subjects, and direct reading links via the Open Library API.

### Intelligent AI Assistant

* Hybrid Deployment: Supports both Google Gemini Pro (Cloud) and Ollama (Local Llama3/Mistral) for privacy and performance.

* Academic Counseling: Specialized in academic regulations, credit calculation, and goal-setting (GPA planning).

### Academic & Financial Ecosystem

* Grade Management: Historical academic performance tracking with 4.0/0.0 scale conversion.

* Curriculum Mapping: Progress tracking against the official major requirements.

* Financial Module: Detailed tuition breakdown, payment history, and E-bill integration.

## 🛠 Tech Stack

| Layer | Technologies |
| ----- | ----- |
| Backend | Python 3.0+, Flask (Modular Blueprint Architecture) |
| Database | SQLAlchemy ORM, SQLite (Production-ready Schema) |
| Frontend | Bootstrap 5, Jinja2 Templates, JavaScript (ES6+), FontAwesome |
| AI/ML | Google Generative AI API, Ollama (Local LLM) |
| Deployment | Gunicorn (WSGI), Render / PythonAnywhere / Ngrok |

## Project Architecture

```
neu_management/
├── app/
│   ├── templates/          # Jinja2 HTML Templates
│   ├── static/             # Assets (CSS, JS, Images)
│   ├── models.py           # Database Schema & ORM Classes
│   ├── auth.py             # Authentication & Session Management
│   ├── home.py             # Dashboard Logic
│   ├── library.py          # Digital Library Module & API Integration
│   └── ai_assistant.py     # AI Logic (Gemini/Ollama)
├── db/
│   └── DBwebSv.db          # SQLite Database File
├── run.py                  # Application Entry Point
├── requirements.txt        # Dependency Manifest
└── Procfile                # WSGI Server Configuration

```

## Quick Start

### . Installation

```
# Clone the repository
git clone https://github.com/log09890/LMS.git
cd LMS

# Setup virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

```

### 2. Configuration

* To use Cloud AI: Obtain a Gemini API Key from Google AI Studio.

* Update app/ai_assistant.py with your key and set USE_LOCAL_AI = False.

### 3. Execution

```
python run.py

```

The application will be accessible at http://localhost:5000.

## Deployment

### PythonAnywhere (Recommended for SQLite)

Clone & Setup: Use the Bash console to clone and create a virtualenv.

WSGI Config: Point the WSGI file to /home/yourusername/LMS/run.py.

Static Mapping: Map /static/ to /home/yourusername/LMS/app/static/.

### Ngrok (For Live Demonstrations)

Run the local server and expose it via:

```
ngrok http 5000

```

## License

Distributed under the MIT License.

Developed for Academic Excellence at NEU.
