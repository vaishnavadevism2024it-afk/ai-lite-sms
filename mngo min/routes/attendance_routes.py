from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils.decorators import login_required, role_required
from utils.db import mongo
from bson.objectid import ObjectId
from datetime import datetime

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    classes = list(mongo.db.classes.find())
    selected_class_id = request.form.get('class_id') or request.args.get('class_id')
    selected_date = request.form.get('date') or request.args.get('date') or datetime.today().strftime('%Y-%m-%d')
    
    students = []
    attendance_record = {}
    
    if selected_class_id:
        # Fetch students for that department/class implicitly (assuming department is used as proxy for now, 
        # or we update students schema. Let's just fetch all by department mapping to class name)
        # For simplicity in this demo, let's fetch students whose 'department' + 'year_sem' + 'section' matches the class name or just show all for now.
        cls = mongo.db.classes.find_one({'_id': ObjectId(selected_class_id)})
        if cls:
            # Simple matching logic: fetch students in same department
            students = list(mongo.db.students.find({'department': cls['department']}))
            
        # Fetch existing attendance record
        record = mongo.db.attendance.find_one({'class_id': selected_class_id, 'date': selected_date})
        if record:
            attendance_record = record.get('statuses', {})
            
    if request.method == 'POST' and 'save_attendance' in request.form:
        if not selected_class_id:
            flash("Select a class first.", "danger")
            return redirect(url_for('attendance.index'))
            
        statuses = {}
        for student in students:
            sid = str(student['_id'])
            # form fields named `status_<student_id>`
            status = request.form.get(f'status_{sid}')
            if status:
                statuses[sid] = status
                
        # Upsert record
        mongo.db.attendance.update_one(
            {'class_id': selected_class_id, 'date': selected_date},
            {'$set': {
                'class_id': selected_class_id,
                'date': selected_date,
                'statuses': statuses,
                'marked_by': request.cookies.get('session', 'Admin')
            }},
            upsert=True
        )
        flash("Attendance successfully saved!", "success")
        return redirect(url_for('attendance.index', class_id=selected_class_id, date=selected_date))
        
    return render_template('attendance/index.html', 
                          classes=classes, 
                          students=students, 
                          selected_class_id=selected_class_id,
                          selected_date=selected_date,
                          attendance_record=attendance_record)
