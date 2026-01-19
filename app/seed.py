from app.database import Base, engine

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

from app.database import SessionLocal
from app.models import Profile, Project

db = SessionLocal()

db.query(Project).delete()
db.query(Profile).delete()
db.commit()

profile = Profile(
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

# ----------- PROJECTS -----------
projects = [
    Project(
        title="Mini Air Purifier",
        description=(
            "Built a compact air purifier using a DC fan and H13 HEPA filter. "
            "Integrated PM2.5 sensor to monitor air quality and controlled fan speed using Arduino."
        ),
        skills="Arduino, PM2.5 Sensor, HEPA Filter"
    ),
    Project(
        title="Archaeology Digsite Management System",
        description=(
            "Developed a database-driven system to manage excavation sites, artifacts, and funding data. "
            "Integrated Maps API for site mapping and implemented login/signup features. "
            "Enabled archaeologists to log and retrieve site and artifact details efficiently."
        ),
        skills="PHP, MySQL, HTML, CSS, Maps API, Authentication"
    ),
    Project(
        title="Byte2Bite – Meal Management Platform",
        description=(
            "Built a platform connecting students with tiffin providers. "
            "Implemented authentication, menu listings, order placement, and REST APIs with Express and MongoDB. "
            "Developed responsive frontend using React with form validation and dynamic components."
        ),
        skills="MongoDB, Express, React, Node.js, REST API, Authentication"
    ),
    Project(
        title="Scoopaloop – Ice Cream Delivery App",
        description=(
            "Created a modern delivery web app with interactive menu browsing, cart management, and smooth order flow. "
            "Used Context API, animated UI with 3D backgrounds, and responsive design."
        ),
        skills="React, Vite, Context API, CSS, UI/UX"
    ),
    Project(
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

print("Database seeded successfully")
