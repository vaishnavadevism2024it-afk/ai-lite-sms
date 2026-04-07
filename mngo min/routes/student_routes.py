from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils.decorators import login_required, role_required
from utils.db import mongo
from bson.objectid import ObjectId

student_bp = Blueprint('student', __name__)

@student_bp.route('/')
@login_required
def index():
    # Fetch all students from MongoDB
    students = list(mongo.db.students.find())
    return render_template('students/list.html', students=students)

@student_bp.route('/add', methods=['GET', 'POST'])
@login_required
@role_required(['admin', 'teacher'])
def add():
    classes = list(mongo.db.classes.find())
    if request.method == 'POST':
        student_data = {
            'student_id': request.form.get('student_id'),
            'full_name': request.form.get('full_name'),
            'gender': request.form.get('gender'),
            'dob': request.form.get('dob'),
            'department': request.form.get('department'),
            'year_sem': request.form.get('year_sem'),
            'section': request.form.get('section'),
            'phone': request.form.get('phone'),
            'parent_contact': request.form.get('parent_contact'),
            'email': request.form.get('email'),
            'address': request.form.get('address'),
        }
        mongo.db.students.insert_one(student_data)
        flash('Student added successfully!', 'success')
        return redirect(url_for('student.index'))
    return render_template('students/form.html', student=None, classes=classes)

@student_bp.route('/edit/<id>', methods=['GET', 'POST'])
@login_required
@role_required(['admin', 'teacher'])
def edit(id):
    student = mongo.db.students.find_one({'_id': ObjectId(id)})
    classes = list(mongo.db.classes.find())
    if not student:
        flash('Student not found.', 'danger')
        return redirect(url_for('student.index'))

    if request.method == 'POST':
        updated_data = {
            'student_id': request.form.get('student_id'),
            'full_name': request.form.get('full_name'),
            'gender': request.form.get('gender'),
            'dob': request.form.get('dob'),
            'department': request.form.get('department'),
            'year_sem': request.form.get('year_sem'),
            'section': request.form.get('section'),
            'phone': request.form.get('phone'),
            'parent_contact': request.form.get('parent_contact'),
            'email': request.form.get('email'),
            'address': request.form.get('address'),
        }
        mongo.db.students.update_one({'_id': ObjectId(id)}, {'$set': updated_data})
        flash('Student updated successfully!', 'success')
        return redirect(url_for('student.index'))
    
    return render_template('students/form.html', student=student, classes=classes)

@student_bp.route('/delete/<id>', methods=['POST'])
@login_required
@role_required(['admin'])
def delete(id):
    result = mongo.db.students.delete_one({'_id': ObjectId(id)})
    if result.deleted_count > 0:
        flash('Student deleted successfully!', 'success')
    else:
        flash('Student not found.', 'danger')
    return redirect(url_for('student.index'))
