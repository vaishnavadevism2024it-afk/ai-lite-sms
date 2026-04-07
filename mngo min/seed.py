from pymongo import MongoClient
from werkzeug.security import generate_password_hash
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/ai_lite_sms')
client = MongoClient(MONGO_URI)
db = client.get_default_database()

def seed_users():
    users_collection = db.users
    
    # Check if admin already exists
    if users_collection.find_one({"username": "admin"}):
        print("Admin user already exists. Skipping.")
    else:
        users = [
            {
                "username": "admin",
                "password_hash": generate_password_hash("admin123"),
                "role": "admin"
            },
            {
                "username": "teacher",
                "password_hash": generate_password_hash("teacher123"),
                "role": "teacher"
            },
            {
                "username": "student",
                "password_hash": generate_password_hash("student123"),
                "role": "student"
            }
        ]
        users_collection.insert_many(users)
        print("Seeded default users (admin, teacher, student).")

if __name__ == "__main__":
    print(f"Connecting to database: {db.name}")
    seed_users()
    print("Database seeding complete.")
