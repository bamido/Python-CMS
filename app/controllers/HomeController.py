from flask import Blueprint, render_template, session, jsonify
from app.config import Config
from app.models.mydb import db
from flask_login import login_required, current_user, login_user

#bp_home = Blueprint('bp_home', __name__, url_prefix='/portal')
bp_home = Blueprint('bp_home', __name__)

@bp_home.route('/dashboard')
@login_required
def dashboard():
    # print("Current user:", current_user)  # Debug statement
    # print("Last name:", current_user.lastname)
    # print("First name:", current_user.firstname)
    # return ''' yeah! '''
    lastname = session.get('lastname')
    firstname = session.get('firstname')
    return render_template('portal/dashboard.html', title='Dashboard', app_name=Config.APP_NAME, author=Config.AUTHOR, lastname=lastname, firstname=firstname)

@bp_home.route('/debug/session')
def debug_session():
    # Print out the session data
    session_data = dict(session)
    return jsonify(session_data)