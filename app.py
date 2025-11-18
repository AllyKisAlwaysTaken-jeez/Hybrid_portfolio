import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
from functools import wraps
from database import SessionLocal, engine, Base
from models import PageContent, User


# DATABASE SETUP

Base.metadata.create_all(bind=engine)

# Pre-populate required sections
def populate_sections():
    db = SessionLocal()
    default_sections = {
        "home": "Welcome to my AI-managed portfolio! I’m passionate about technology, innovation, and building impactful solutions.",
        "about": "I am a Computer Science postgraduate specializing in AI and software development.",
        "projects": "This section highlights my portfolio projects and technical work, including apps, tools, and research projects.",
        "contact": "Feel free to reach out through email, LinkedIn, or my contact form. Email: example@outlook.com"
    }
    for section, content in default_sections.items():
        existing = db.query(PageContent).filter(PageContent.section == section).first()
        if not existing:
            db.add(PageContent(section=section, content=content))
    db.commit()
    db.close()

populate_sections()  # Runs automatically on app start


# FLASK APP

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Change in production
app.config["TEMPLATES_AUTO_RELOAD"] = True


# AGENT AI (OpenAI API)

import requests

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def generate_text(prompt: str, max_length: int = 180) -> str:
    if not OPENAI_API_KEY:
        return "❌ Missing API key. Please set your OPENAI_API_KEY environment variable."

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a portfolio content rewriting assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": max_length
    }

    response = requests.post(url, headers=headers, json=payload)
    try:
        data = response.json()
    except Exception as e:
        return f"❌ Failed to parse API response: {str(e)}"
    if "error" in data:
        return f"❌ OpenAI API error: {data['error'].get('message', 'Unknown error')}"
    if "choices" not in data or len(data["choices"]) == 0:
        return f"❌ Unexpected API response: {data}"
    return data["choices"][0]["message"]["content"]


# HELPER FUNCTIONS

def save_content(section, text):
    db = SessionLocal()
    existing = db.query(PageContent).filter(PageContent.section == section).first()
    if existing:
        existing.content = text
    else:
        db.add(PageContent(section=section, content=text))
    db.commit()
    db.close()

def get_content(section, default_text):
    db = SessionLocal()
    entry = db.query(PageContent).filter(PageContent.section == section).first()
    db.close()
    return entry.content if entry else default_text

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user" not in session:
            flash("Please log in to access the dashboard.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


# ROUTES

@app.route("/")
def home():
    home_intro = get_content("home", "Welcome to my AI-managed portfolio!")
    return render_template("index.html", home_intro=home_intro, current_year=datetime.now().year)

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", current_year=datetime.now().year)

@app.route("/ai-rewrite", methods=["GET", "POST"])
@login_required
def ai_rewrite():
    rewritten_text = None
    if request.method == "POST":
        section = request.form["section"]
        job_role = request.form["job_role"]
        keywords = request.form.get("keywords", "")
        project_info = request.form.get("project_info", "")
        prompt = (
            f"Rewrite the '{section}' section of a portfolio website for someone applying "
            f"as a {job_role}. Use these keywords: {keywords}. "
            f"Include project details if relevant: {project_info}. "
            f"Tone: professional, engaging, clear."
        )
        rewritten_text = generate_text(prompt, max_length=300)
        flash("AI-generated text created!", "success")
        save_content(section, rewritten_text)
    return render_template("dashboard.html", rewritten_text=rewritten_text, current_year=datetime.now().year)


# LOGIN / LOGOUT

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = SessionLocal()
        user = db.query(User).filter(User.username==username, User.password==password).first()
        db.close()
        if user:
            session["user"] = username
            flash("Logged in successfully!", "success")
            return redirect(url_for("dashboard"))
        flash("Invalid username or password.", "danger")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
