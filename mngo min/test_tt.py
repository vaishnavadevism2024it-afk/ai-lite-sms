from app import app
from utils.db import mongo
from utils.timetable_engine import generate_timetable_data

with app.app_context():
    classes = list(mongo.db.classes.find())
    subjects = list(mongo.db.subjects.find())
    print("Classes:", len(classes))
    print("Subjects:", len(subjects))
    if classes and subjects:
        generated = generate_timetable_data(classes, subjects)
        mongo.db.timetable.update_one(
            {"active": True},
            {"$set": {"schedule": generated, "active": True}},
            upsert=True
        )
        print("Generated and saved successfully.")
    else:
        print("Not enough data to generate.")
