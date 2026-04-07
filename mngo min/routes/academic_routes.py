from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils.decorators import login_required, role_required
from utils.db import mongo
from bson.objectid import ObjectId

academic_bp = Blueprint('academic', __name__)

# --- DEPARTMENTS & CLASSES ---

@academic_bp.route('/classes')
@login_required
def classes_index():
    classes = list(mongo.db.classes.find())
    departments = list(mongo.db.departments.find())
    return render_template('academic/classes.html', classes=classes, departments=departments)

@academic_bp.route('/classes/add', methods=['POST'])
@login_required
@role_required(['admin'])
def add_class():
    class_data = {
        'name': request.form.get('name'), # e.g., 'IT 2nd Year A'
        'department': request.form.get('department'),
        'semester': request.form.get('semester')
    }
    mongo.db.classes.insert_one(class_data)
    flash('Class added successfully!', 'success')
    return redirect(url_for('academic.classes_index'))

@academic_bp.route('/classes/delete/<id>', methods=['POST'])
@login_required
@role_required(['admin'])
def delete_class(id):
    mongo.db.classes.delete_one({'_id': ObjectId(id)})
    flash('Class removed!', 'success')
    return redirect(url_for('academic.classes_index'))

# --- SUBJECTS ---

@academic_bp.route('/subjects')
@login_required
def subjects_index():
    subjects = list(mongo.db.subjects.find())
    classes = list(mongo.db.classes.find())
    teachers = list(mongo.db.teachers.find())
    return render_template('academic/subjects.html', subjects=subjects, classes=classes, teachers=teachers)

@academic_bp.route('/subjects/add', methods=['POST'])
@login_required
@role_required(['admin'])
def add_subject():
    subject_data = {
        'subject_code': request.form.get('subject_code'),
        'subject_name': request.form.get('subject_name'),
        'class_id': request.form.get('class_id'),
        'teacher_id': request.form.get('teacher_id'),
        'weekly_hours': int(request.form.get('weekly_hours')),
        'type': request.form.get('type') # Theory / Lab
    }
    mongo.db.subjects.insert_one(subject_data)
    flash('Subject assigned successfully!', 'success')
    return redirect(url_for('academic.subjects_index'))

@academic_bp.route('/subjects/delete/<id>', methods=['POST'])
@login_required
@role_required(['admin'])
def delete_subject(id):
    mongo.db.subjects.delete_one({'_id': ObjectId(id)})
    flash('Subject mapping removed!', 'success')
    return redirect(url_for('academic.subjects_index'))
