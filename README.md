# Automated Event Planner and Approval System - Phase 4

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-2.x-lightgrey?logo=flask)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Managed-blue?logo=postgresql)
![Git](https://img.shields.io/badge/Version%20Control-Git-orange?logo=git)
![AI-Assisted](https://img.shields.io/badge/Development-AI--Assisted-green?logo=google-gemini)

## 📋 Executive Summary
The goal of this project is to digitize institutional workflows at **JNU Jaipur**, replacing traditional paper-based event approval processes with a transparent, efficient, and auditable digital system (ref. Section 3.2). Phase 4 focuses on the full automation of the multi-level approval pipeline, ensuring that every institutional event follows a strict hierarchy of validation from Faculty to Department Head.

## 🚀 Phase 4 Scope: Approval Workflow Automation
This phase implements the core state machine that governs the lifecycle of an event:
- **State Machine**: Multi-level transitions: `Draft` → `Pending Faculty` → `Pending Dept Head` → `Approved` / `Rejected`.
- **Role-Based Decisions**: Specialized dashboards for Faculty, Department Heads, and Students with conditional UI rendering.
- **Audit & History**: Detailed tracking of every decision via the `Approvals` entity, including timestamped comments.
- **Database Schema**: Expanded schema featuring the `Approvals` entity and dynamic status fields in the `Events` model.

## 🛠 Tech Stack
- **Backend**: Python 3.8+, Flask 2.x, SQLAlchemy (ORM)
- **Frontend**: Jinja2, HTML5, Vanilla CSS3 (Modern Glassmorphism Design), JavaScript
- **Database**: PostgreSQL (Production/Supabase), SQLite (Local/Development)
- **Deployment**: Gunicorn (WSGI Server)

## 💻 Installation Guide
Follow these steps to set up the project locally:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/CyberSential22/epas-phase-4.git
   cd epas-phase-4
   ```

2. **Set Up Virtual Environment**:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/macOS
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**:
   Create a `.env` file in the root directory:
   ```env
   FLASK_APP=run.py
   FLASK_ENV=development
   SECRET_KEY=yoursecretkey
   ```

5. **Run Locally**:
   ```bash
   python run.py
   ```

## 📂 Project Structure
```
epas-phase-4/
├── app/
│   ├── blueprints/    # Modular route logic (Admin, Auth, Events, etc.)
│   ├── models/        # SQLAlchemy Database models (Event, Approval, User)
│   ├── static/        # CSS, Images, and JS assets
│   ├── templates/     # Jinja2 HTML templates
│   ├── utils/         # Helper functions (logging, workflow engine)
│   └── __init__.py    # App factory initialization
├── instance/          # Local SQLite DB and sensitive files
├── requirements.txt   # Dependency list
├── run.py             # Entry point for execution
└── vercel.json        # Frontend proxy configuration
```

## 🌐 Deployment Overview
- **Vercel**: Acts as the frontend proxy, handling SSL and forwarding requests to the backend.
- **Render**: Hosts the Flask backend via Gunicorn on a high-availability environment.
- **Supabase**: Managed PostgreSQL database providing a robust, scalable storage layer.

## 🎓 Acknowledgments
- **Project Team**: Kashif Shaikh, Aditya Gond, Yaduvansh Singh Ranawat (JNU Jaipur).
- **Guide**: Ms. Saumya.
- **AI-Assisted Development**: Developed with the ethical use of AI-assisted tools for research and debugging, maintaining student ownership of core architecture and design (Section 6.5).

## 📄 License
This project is licensed under the [MIT License](LICENSE).
