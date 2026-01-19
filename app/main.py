from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os




from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import models

from typing import Optional

from sqlalchemy import or_

from collections import Counter

app = FastAPI(title="Me-API Playground")



# Serve static files from app/frontend
app.mount("/frontend", StaticFiles(directory="app/frontend"), name="frontend")
@app.get("/")
def root():
    return FileResponse(os.path.join("app/frontend", "index.html"))




from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


from pydantic import BaseModel

class ProfileUpdate(BaseModel):
    name: str
    email: str
    education: str
    github: str
    linkedin: str
    portfolio: str




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/profile")
def get_profile(db: Session = Depends(get_db)):
    profile = db.query(models.Profile).first()
    return profile



from fastapi import HTTPException

@app.put("/profile")
def update_profile(
    data: ProfileUpdate,
    db: Session = Depends(get_db)
):
    profile = db.query(models.Profile).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    for key, value in data.dict().items():
        setattr(profile, key, value)

    db.commit()
    db.refresh(profile)
    return profile


@app.get("/projects")
def get_projects(skill: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.Project)

    if skill:
        query = query.filter(models.Project.skills.contains(skill.lower()))

    return query.all()



@app.get("/search")
def search(q: str, db: Session = Depends(get_db)):
    results = {}

    profile = db.query(models.Profile).filter(
        models.Profile.name.contains(q)
    ).first()

    projects = db.query(models.Project).filter(
        or_(
            models.Project.title.contains(q),
            models.Project.description.contains(q)
        )
    ).all()

    results["profile"] = profile
    results["projects"] = projects

    return results



@app.get("/skills")
def get_skills(db: Session = Depends(get_db)):
    projects = db.query(models.Project).all()  # use models.Project

    skill_count = {}
    for project in projects:
        if not project.skills:
            continue
        for skill in project.skills.split(","):
            skill = skill.strip().lower()
            if skill:
                skill_count[skill] = skill_count.get(skill, 0) + 1

    return skill_count
