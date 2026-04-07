from flask import Flask, redirect, url_for
from config import Config
from utils.db import init_db

# App Initialization
app = Flask(__name__)
app.config.from_object(Config)

# Initialize Database
init_db(app)

# Register Blueprints
from routes.auth_routes import auth_bp
from routes.dash_routes import dash_bp
from routes.student_routes import student_bp
from routes.teacher_routes import teacher_bp
from routes.academic_routes import academic_bp
from routes.timetable_routes import timetable_bp
from routes.attendance_routes import attendance_bp
from routes.notice_routes import notice_bp
from routes.face_routes import face_bp

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(dash_bp, url_prefix='/dashboard')
app.register_blueprint(student_bp, url_prefix='/students')
app.register_blueprint(teacher_bp, url_prefix='/teachers')
app.register_blueprint(academic_bp, url_prefix='/academic')
app.register_blueprint(timetable_bp, url_prefix='/timetable')
app.register_blueprint(attendance_bp, url_prefix='/attendance')
app.register_blueprint(notice_bp, url_prefix='/notice')
app.register_blueprint(face_bp, url_prefix='/face')

import webbrowser
from threading import Timer

@app.route('/')
def home():
    # Redirect base URL to dashboard or login
    return redirect(url_for('dashboard.index'))

def open_browser():
      webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run(debug=True, port=5000, use_reloader=False)