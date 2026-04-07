from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils.decorators import login_required, role_required
from utils.db import mongo
import datetime

notice_bp = Blueprint('notice', __name__)

@notice_bp.route('/')
@login_required
def index():
    notices = list(mongo.db.notices.find().sort("date", -1))
    return render_template('notices/index.html', notices=notices)

@notice_bp.route('/send', methods=['POST'])
@login_required
@role_required(['admin'])
def send_notice():
    title = request.form.get('title')
    message = request.form.get('message')
    audience = request.form.get('audience')
    
    notice_data = {
        'title': title,
        'message': message,
        'audience': audience,
        'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'status': 'Sent'
    }
    
    # In a real deployed environment, this is where we would trigger the Telegram Bot API
    # e.g., requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": chat_id, "text": message})
    
    mongo.db.notices.insert_one(notice_data)
    flash("Notice Broadcasted Successfully! (Telegram integration stubbed)", "success")
    return redirect(url_for('notice.index'))
