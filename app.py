from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from datetime import datetime
from database import SessionLocal, engine, Base
from models import PageContent
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")

Base.metadata.create_all(bind=engine)

# Utility: fetch content from database or fallback text
def get_content(page_name, fallback):
    db = SessionLocal()
    page = db.query(PageContent).filter_by(page_name=page_name).first()
    db.close()
    return page.content if page else fallback


# Main Public Pages


@app.route("/")
def home():
    home_content = get_content("home", "Welcome to my portfolio website!")
    return render_template("index.html",
                           home_content=home_content,
                           current_year=datetime.now().year)


@app.route("/about")
def about():
    about_content = get_content(
        "about", 
        "I am a Computer Science postgraduate specializing in AI and software development."
    )
    return render_template("about.html",
                           about_content=about_content,
                           current_year=datetime.now().year)


@app.route("/projects")
def projects():
    projects_content = get_content(
        "projects", 
        "Here are some projects I’ve been working on."
    )
    return render_template("projects.html",
                           projects_content=projects_content,
                           current_year=datetime.now().year)


@app.route("/contact")
def contact():
    contact_content = get_content(
        "contact", 
        "You can reach me through email or my social accounts."
    )
    return render_template("contact.html",
                           contact_content=contact_content,
                           current_year=datetime.now().year)



# Dashboard + Login


@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    db = SessionLocal()
    pages = db.query(PageContent).all()
    db.close()

    return render_template("dashboard.html",
                           pages=pages,
                           current_year=datetime.now().year)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["password"] == os.environ.get("ADMIN_PASSWORD", "admin"):
            session["logged_in"] = True
            return redirect(url_for("dashboard"))
        return render_template("login.html", error="Incorrect password.")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))



# Hybrid Agent + Assistant APIs


@app.route("/ai-rewrite", methods=["POST"])
def ai_rewrite():
    """Agent rewrites portfolio sections."""
    data = request.json
    page = data.get("page")
    content = data.get("content")

    db = SessionLocal()
    page_model = db.query(PageContent).filter_by(page_name=page).first()

    if not page_model:
        page_model = PageContent(page_name=page, content=content)
        db.add(page_model)
    else:
        page_model.content = content

    db.commit()
    db.close()

    return jsonify({"message": "Content saved", "page": page})


@app.route("/assistant-advice", methods=["POST"])
def assistant_advice():
    """Assistant gives feedback (this returns text only)."""
    data = request.json
    user_text = data.get("content")

    feedback = (
        "Great start! Try adding more measurable achievements and consider "
        "including a short intro sentence to add personality."
    )

    return jsonify({"advice": feedback})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
