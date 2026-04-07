from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils.decorators import login_required, role_required
from utils.db import mongo
from bson.objectid import ObjectId

teacher_bp = Blueprint('teacher', __name__)

@teacher_bp.route('/')
@login_required
def index():
    teachers = list(mongo.db.teachers.find())
    return render_template('teachers/list.html', teachers=teachers)

@teacher_bp.route('/add', methods=['GET', 'POST'])
@login_required
@role_required(['admin'])
def add():
    if request.method == 'POST':
        teacher_data = {
            'teacher_id': request.form.get('teacher_id'),
            'full_name': request.form.get('full_name'),
            'department': request.form.get('department'),
            'specialization': request.form.get('specialization'),
            'phone': request.form.get('phone'),
            'email': request.form.get('email'),
            'available_hours': request.form.get('available_hours'),
            'max_classes': request.form.get('max_classes', type=int),
        }
        mongo.db.teachers.insert_one(teacher_data)
        flash('Teacher added successfully!', 'success')
        return redirect(url_for('teacher.index'))
    return render_template('teachers/form.html', teacher=None)

@teacher_bp.route('/edit/<id>', methods=['GET', 'POST'])
@login_required
@role_required(['admin'])
def edit(id):
    teacher = mongo.db.teachers.find_one({'_id': ObjectId(id)})
    if not teacher:
        flash('Teacher not found.', 'danger')
        return redirect(url_for('teacher.index'))

    if request.method == 'POST':
        updated_data = {
            'teacher_id': request.form.get('teacher_id'),
            'full_name': request.form.get('full_name'),
            'department': request.form.get('department'),
            'specialization': request.form.get('specialization'),
            'phone': request.form.get('phone'),
            'email': request.form.get('email'),
            'available_hours': request.form.get('available_hours'),
            'max_classes': request.form.get('max_classes', type=int),
        }
        mongo.db.teachers.update_one({'_id': ObjectId(id)}, {'$set': updated_data})
        flash('Teacher updated successfully!', 'success')
        return redirect(url_for('teacher.index'))
    
    return render_template('teachers/form.html', teacher=teacher)

@teacher_bp.route('/delete/<id>', methods=['POST'])
@login_required
@role_required(['admin'])
def delete(id):
    mongo.db.teachers.delete_one({'_id': ObjectId(id)})
    flash('Teacher deleted successfully!', 'success')
    return redirect(url_for('teacher.index'))
