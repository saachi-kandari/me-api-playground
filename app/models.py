from sqlalchemy import Column, Integer, String
from app.database import Base

class Profile(Base):
    __tablename__ = "profile"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    education = Column(String)
    github = Column(String)
    linkedin = Column(String)
    portfolio = Column(String)

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    skills = Column(String) 
