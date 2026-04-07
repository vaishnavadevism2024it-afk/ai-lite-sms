from flask import Blueprint, render_template
from utils.decorators import login_required
from utils.db import mongo

dash_bp = Blueprint('dashboard', __name__)

@dash_bp.route('/')
@login_required
def index():
    # Placeholder statistics fetching
    total_students = mongo.db.students.count_documents({}) if 'students' in mongo.db.list_collection_names() else 0
    total_teachers = mongo.db.teachers.count_documents({}) if 'teachers' in mongo.db.list_collection_names() else 0
    total_departments = mongo.db.departments.count_documents({}) if 'departments' in mongo.db.list_collection_names() else 0
    total_subjects = mongo.db.subjects.count_documents({}) if 'subjects' in mongo.db.list_collection_names() else 0

    return render_template('dashboard.html', 
                           students=total_students, 
                           teachers=total_teachers, 
                           departments=total_departments, 
                           subjects=total_subjects)
