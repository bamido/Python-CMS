from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.UserModel import UserModel
from app.config import Config
from app.models.mydb import db
from flask_login import login_required, current_user, login_user
from werkzeug.utils import secure_filename
import os
import uuid

bp_user = Blueprint('usercontroller', __name__)

@bp_user.route('/users')
def listusers():
    # get all users
    users = UserModel.get_all_users()
    return render_template('rbac/listusers.html', users=users, title="Users")


@login_required
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_IMG_EXTENSIONS


@bp_user.route('/profilephoto', methods=['GET', 'POST'])
@login_required
def uploadprofilephoto():
    if request.method == 'POST':
        # Check if file part is present
        if 'profile_photo' not in request.files:
            flash('No file part')
            return redirect(request.url)

        # Get the uploaded file
        file = request.files['profile_photo']

        # Check if user selected a file
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        # Check allowed extensions
        if file and allowed_file(file.filename):
            #filename = secure_filename(file.filename)  # Sanitize filename
            # Generate a unique filename (optional)
            filename, ext = os.path.splitext(file.filename)  # Split filename and extension
            new_filename = secure_filename(filename + '_' + str(uuid.uuid4()) + ext)  # Add a UUID
            file.save(os.path.abspath(os.path.join(Config.PROFILE_PHOTO_DIR, new_filename)))
            flash('Profile photo uploaded successfully!')
            current_user.photograph = new_filename
            db.session.commit()

            return redirect(url_for('usercontroller.uploadprofilephoto'))  # Redirect to same page
        else:
            flash('Extension not allowed!')
            return redirect(request.url)

    return render_template('rbac/profilephoto.html', moduletitle="User Management", title='Profile Photo', app_name=Config.APP_NAME, author=Config.AUTHOR, current_user=current_user)
