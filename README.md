# ME-API-PLAYGROUND

A personal portfolio API built with **FastAPI** and **SQLite**, showcasing my profile, projects, and skills. Includes a simple frontend for interactive browsing.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [API Endpoints](#api-endpoints)
- [Frontend](#frontend)
- [Built With](#built-with)

---

## Project Overview

This project serves as a personal portfolio backend with:

- A profile endpoint showing my personal and educational info.
- Projects endpoint showing all projects with title, description, and skills.
- Skills endpoint summarizing skills across projects.
- Search functionality by project title, description, or name.

---

## Features

- Auto-create database tables on startup.
- Auto-seed profile and project data if database is empty.
- CRUD support for profile (update via PUT request).
- CORS enabled for frontend integration.
- Simple responsive frontend using HTML, CSS, and JavaScript.

---

## Project Structure

```
ME-API-PLAYGROUND/
├─ app/
│ ├─ frontend/
│ │ └─ index.html
│ ├─ init.py
│ ├─ create_tables.py
│ ├─ database.py
│ ├─ main.py
│ ├─ models.py
│ ├─ schemas.py
│ └─ seed.py
├─ venv/
├─ me.db
├─ requirements.txt
└─ .gitignore
```
## Setup Instructions

1. **Clone the repository**
git clone <your-repo-url>
cd ME-API-PLAYGROUND

2. **Create a virtual environment**
python -m venv venv

3. **Activate the virtual environment**
Windows: 
venv\Scripts\activate
Mac/Linux:
source venv/bin/activate

3. **Install dependencies**
pip install -r requirements.txt

4. **pip install -r requirements.txt**
uvicorn app.main:app --reload

5. **Run the application**
uvicorn app.main:app --reload

6. **Open frontend**
Visit http://127.0.0.1:8000/frontend in your browser.

## API Endpoints

| Endpoint     | Method | Description                                      |
|-------------|--------|--------------------------------------------------|
| /health     | GET    | Check API health                                 |
| /profile    | GET    | Fetch profile information                        |
| /profile    | PUT    | Update profile information                       |
| /projects   | GET    | Fetch all projects, optional query param `skill` to filter |
| /skills     | GET    | Fetch top skills summary across projects        |
| /search     | GET    | Search profile and projects by query string `q` |

## Frontend 

Located in app/frontend/index.html

Uses vanilla JavaScript to fetch data from API endpoints.

Displays profile, projects, and top skills dynamically.

## Built With

FastAPI

SQLite

SQLAlchemy

HTML, CSS, JavaScript

Uvicorn (for server)

## Future Scope

- Add authentication for profile editing.
- Allow adding new projects via API.
- Add filtering and sorting for projects by skill or date.
- Improve frontend UI/UX with animations and responsive design.
- Deploy with a proper domain and HTTPS support.


## Links

- **Live Hosted Project:** [https://me-api-playground-skmz.onrender.com/](https://me-api-playground-skmz.onrender.com/)
- **GitHub Repository:** [git@github.com:saachi-kandari/me-api-playground.git](git@github.com:saachi-kandari/me-api-playground.git)


## Author
Saachi Kandari