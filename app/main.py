
from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional
import os

from app.database import SessionLocal, engine
from app.models import Base, Profile, Project
from pydantic import BaseModel

app = FastAPI(title="Me-API Playground")

# Serve frontend static files
app.mount("/frontend", StaticFiles(directory="app/frontend"), name="frontend")

@app.get("/")
def root():
    return FileResponse(os.path.join("app/frontend", "index.html"))

# ------------------- CORS -------------------
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------- Database -------------------
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables if they don't exist (no auto-seeding!)
Base.metadata.create_all(bind=engine)

# ------------------- Models -------------------
class ProfileUpdate(BaseModel):
    name: str
    email: str
    education: str
    github: str
    linkedin: str
    portfolio: str

# ------------------- Routes -------------------
@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/profile")
def get_profile(db: Session = Depends(get_db)):
    profile = db.query(Profile).first()
    return profile

@app.put("/profile")
def update_profile(data: ProfileUpdate, db: Session = Depends(get_db)):
    profile = db.query(Profile).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    for key, value in data.dict().items():
        setattr(profile, key, value)
    db.commit()
    db.refresh(profile)
    return profile

@app.get("/projects")
def get_projects(skill: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Project)
    if skill:
        query = query.filter(Project.skills.contains(skill.lower()))
    return query.all()

@app.get("/search")
def search(q: str, db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.name.contains(q)).first()
    projects = db.query(Project).filter(
        or_(Project.title.contains(q), Project.description.contains(q))
    ).all()
    return {"profile": profile, "projects": projects}

@app.get("/skills")
def get_skills(db: Session = Depends(get_db)):
    projects = db.query(Project).all()
    skill_count = {}
    for project in projects:
        if not project.skills:
            continue
        for skill in project.skills.split(","):
            skill = skill.strip().lower()
            if skill:
                skill_count[skill] = skill_count.get(skill, 0) + 1
    return skill_count
