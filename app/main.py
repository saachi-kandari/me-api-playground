from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
# 
from app.database import engine
from app import models

# Create tables if they don't exist
models.Base.metadata.create_all(bind=engine)
# 



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




@app.on_event("startup")
def startup_event():
    # 1. Create tables if they don't exist
    Base.metadata.create_all(bind=engine)

    # 2. Start session
    db = SessionLocal()

    # 3. Check if profile exists
    if db.query(models.Profile).count() == 0:
        profile = models.Profile(
            name="Saachi Kandari",
            email="231210088@nitdelhi.ac.in",
            education=(
                "National Institute of Technology, Delhi – B.Tech in Computer Science and Engineering, "
                "Army Public School, Dhaula Kuan – 12th Grade: 94.2%, 10th Grade: 94.8%"
            ),
            github="https://github.com/saachi-kandari",
            linkedin="https://www.linkedin.com/in/saachi-k-0648b8288",
            portfolio="https://saachikandari.com"
        )
        db.add(profile)

    # 4. Check if projects exist
    if db.query(models.Project).count() == 0:
        projects = [
            models.Project(
                title="Mini Air Purifier",
                description=(
                    "Built a compact air purifier using a DC fan and H13 HEPA filter. "
                    "Integrated PM2.5 sensor to monitor air quality and controlled fan speed using Arduino."
                ),
                skills="Arduino, PM2.5 Sensor, HEPA Filter"
            ),
            models.Project(
                title="Archaeology Digsite Management System",
                description=(
                    "Developed a database-driven system to manage excavation sites, artifacts, and funding data. "
                    "Integrated Maps API for site mapping and implemented login/signup features. "
                    "Enabled archaeologists to log and retrieve site and artifact details efficiently."
                ),
                skills="PHP, MySQL, HTML, CSS, Maps API, Authentication"
            ),
            models.Project(
                title="Byte2Bite – Meal Management Platform",
                description=(
                    "Built a platform connecting students with tiffin providers. "
                    "Implemented authentication, menu listings, order placement, and REST APIs with Express and MongoDB. "
                    "Developed responsive frontend using React with form validation and dynamic components."
                ),
                skills="MongoDB, Express, React, Node.js, REST API, Authentication"
            ),
            models.Project(
                title="Scoopaloop – Ice Cream Delivery App",
                description=(
                    "Created a modern delivery web app with interactive menu browsing, cart management, and smooth order flow. "
                    "Used Context API, animated UI with 3D backgrounds, and responsive design."
                ),
                skills="React, Vite, Context API, CSS, UI/UX"
            ),
            models.Project(
                title="NGO Student Management Platform (Hackathon)",
                description=(
                    "Contributed to a full-stack platform for an NGO to manage students, campaigns, donations, and admin workflows. "
                    "Built dashboards, chatbot interface, student data forms with voice input, and admin panel features."
                ),
                skills="MERN Stack, Dashboards, Admin Panel"
            )
        ]
        db.add_all(projects)

    db.commit()
    db.close()
    print("Database auto-seeded if empty")





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
