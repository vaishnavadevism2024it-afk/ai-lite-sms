from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils.decorators import login_required, role_required
from utils.db import mongo
from utils.timetable_engine import generate_timetable_data
from bson.objectid import ObjectId

timetable_bp = Blueprint('timetable', __name__)

@timetable_bp.route('/')
@login_required
def index():
    classes = list(mongo.db.classes.find())
    teachers = {str(t['_id']): t['full_name'] for t in mongo.db.teachers.find()}
    
    # Try fetching existing timetable from DB
    saved_schedule = mongo.db.timetable.find_one({"active": True})
    
    selected_class_id = request.args.get('class_id')
    display_table = None

    if saved_schedule and selected_class_id:
        if selected_class_id in saved_schedule.get('schedule', {}):
            display_table = saved_schedule['schedule'][selected_class_id]

    return render_template('timetable/view.html', 
                           classes=classes, 
                           teachers=teachers,
                           selected_class_id=selected_class_id,
                           display_table=display_table,
                           has_schedule=bool(saved_schedule))

@timetable_bp.route('/generate', methods=['POST'])
@login_required
@role_required(['admin'])
def generate():
    classes = list(mongo.db.classes.find())
    subjects = list(mongo.db.subjects.find())
    
    if not classes or not subjects:
        flash("Need at least 1 class and 1 subject assigned to generate a timetable.", "warning")
        return redirect(url_for('timetable.index'))
        
    generated = generate_timetable_data(classes, subjects)
    
    # Save to DB
    mongo.db.timetable.update_one(
        {"active": True},
        {"$set": {"schedule": generated, "active": True}},
        upsert=True
    )
    
    flash("Smart Timetable Generated Successfully! (AI-Lite Rules Applied)", "success")
    return redirect(url_for('timetable.index'))
