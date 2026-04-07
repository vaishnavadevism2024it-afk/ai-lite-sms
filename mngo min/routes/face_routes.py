from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils.decorators import login_required, role_required
from utils.face_core import simulate_face_scan
import datetime

face_bp = Blueprint('face', __name__)

@face_bp.route('/')
@login_required
def index():
    return render_template('face/index.html')

@face_bp.route('/scan', methods=['POST'])
@login_required
def scan():
    result = simulate_face_scan()
    if result.get('status') == 'success':
        flash(f"Face Recognized: {result['name']} ({result['student_id']}) with {result['confidence']} confidence.", "success")
        # Here we would normally save to MongoDB attendance collection automatically
    else:
        flash(f"Face Scan Failed or Error: {result.get('message', 'Unknown Error')}", "danger")
        
    return redirect(url_for('face.index'))
