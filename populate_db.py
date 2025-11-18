from database import SessionLocal, Base, engine
from models import PageContent

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Predefined sections with default content
default_sections = {
    "home": "Welcome to my AI-managed portfolio! I’m passionate about technology, innovation, and building impactful solutions.",
    "about": "I am a Computer Science postgraduate specializing in AI and software development.",
    "projects": "This section highlights my portfolio projects and technical work, including apps, tools, and research projects.",
    "contact": "Feel free to reach out through email, LinkedIn, or my contact form. Email: example@outlook.com"
}

def populate_sections():
    db = SessionLocal()
    for section, content in default_sections.items():
        # Check if section already exists
        existing = db.query(PageContent).filter(PageContent.section == section).first()
        if not existing:
            db.add(PageContent(section=section, content=content))
    db.commit()
    db.close()
    print("Database pre-populated with default sections.")

if __name__ == "__main__":
    populate_sections()
