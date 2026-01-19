from pydantic import BaseModel

class ProfileBase(BaseModel):
    name: str
    email: str
    education: str
    github: str
    linkedin: str
    portfolio: str

class ProfileCreate(ProfileBase):
    pass

class Profile(ProfileBase):
    id: int

    class Config:
        orm_mode = True

class Project(BaseModel):
    id: int
    title: str
    description: str
    skills: str

    class Config:
        orm_mode = True
