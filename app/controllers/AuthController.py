from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.UserModel import UserModel, SignupForm, LoginForm
from app.config import Config
from app.models.mydb import db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, logout_user
#from app import login_manager


bp_authcontroller = Blueprint('bp_authcontroller', __name__)


@bp_authcontroller.route('/')
@bp_authcontroller.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':        
        username_or_email = request.form['username_or_email']
        password = request.form['password']
        # check if username/email address exists
        user = UserModel.query.filter((UserModel.username == username_or_email) | (UserModel.email_address == username_or_email)).first()        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.user_id            
            session['username'] = user.username
            session['email_address'] = user.email_address
            session['firstname'] = user.firstname
            session['lastname'] = user.lastname

            # print(user.lastname)
            # print(user.firstname)
            # print(user.email_address)
            login_user(user, remember=form.remember.data)
            return redirect(url_for('bp_home.dashboard'))
        else:
            flash('Invalid login credentials. <br> Please try again!', 'danger')
    return render_template('auth/signin.html', title='Sign In', app_name=Config.APP_NAME, author=Config.AUTHOR,form=form)


@bp_authcontroller.route('/register', methods=['GET', 'POST'])
def register():
    form = SignupForm(request.form)
    #print(request.form)
    if request.method == 'POST' and form.validate():
        # Extract data from the form
        username = form.username.data
        email = form.email_address.data
        password = form.password.data
        lastname = form.lastname.data
        firstname = form.firstname.data

        # Check if the email already exists in the database
        existing_user = UserModel.query.filter_by(email_address=email).first()
        if existing_user:
            # Handle duplicate email address (e.g., display an error message)
            flash('Email address already exists.', 'error')            
            return render_template('auth/signup.html', title='Sign Up', app_name=Config.APP_NAME, author=Config.AUTHOR, form=form)


        # If the email address doesn't exist, proceed with inserting the new record
        try:
            # Create a new user object
            hashed_password = generate_password_hash(password)
            new_user = UserModel(
                username=username,
                email_address=email,
                password=hashed_password,
                lastname=lastname,
                firstname=firstname,
                role_id=3
            )

            db.session.add(new_user)
            db.session.commit()
            msg = "Hello {} {}, your account has been successfully created! Please use the form below to log in."
            flash(msg.format(firstname, lastname), 'success')
            form = LoginForm(request.form)
            return render_template('auth/signin.html', title='Sign In', app_name=Config.APP_NAME, author=Config.AUTHOR, msg=msg, form=form)
        except IntegrityError as e:
            # Handle IntegrityError (e.g., rollback the transaction, display an error message)
            db.session.rollback()
            error_info = e.orig.args  # Get the original error message
            flash(f'Error: {error_info}', 'error')
            return render_template('auth/signup.html', title='Sign Up', app_name=Config.APP_NAME, author=Config.AUTHOR, form=form)

    return render_template('auth/signup.html', title='Sign Up', app_name=Config.APP_NAME, author=Config.AUTHOR, form=form)

@bp_authcontroller.route('/logout')
def logout():
    logout_user()
    # Redirect the user to the login page after logout
    return redirect(url_for('bp_authcontroller.login'))    