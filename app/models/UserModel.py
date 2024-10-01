from app.models.mydb import db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email
from flask_login import UserMixin

from app.models.RoleModel import RoleModel
from app.models.ModuleModel import ModuleModel
from app.models.TaskModel import TaskModel
from app.models.PrivilegeModel import PrivilegeModel


class UserModel(UserMixin, db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email_address = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    phonenumber = db.Column(db.String(20))
    dateofbirth = db.Column(db.Date)
    created_at = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    photograph = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return '<UserModel {}>'.format(self.user_id)

    def __init__(self, user_id=None, username=None, email_address=None, password=None, lastname=None, firstname=None, role_id=3):
        self.user_id = user_id
        self.username = username
        self.email_address = email_address
        self.password = password
        self.lastname = lastname
        self.firstname = firstname
        self.role_id = role_id
   
    
    def get_id(self):
        return str(self.user_id) # Return the user ID as a string

    @staticmethod
    def get_user_by_username(username):
        # Query the UserModel to retrieve the user by username
        user = UserModel.query.filter_by(username=username).first()
        return user

    def get_all_users():
        # Sample method to retrieve all users
        return ["Elon Musk", "Tim Cook", "Larry Page", 'Yemi Bamido', 'Toluwani Bamido']  # Example data

    def print_model_columns(themodel):
        column_names = [attr for attr in dir(themodel) if not callable(getattr(themodel, attr)) and not attr.startswith("__")]
        print(f"Model Columns: {', '.join(column_names)}")

    def get_user_tasks(role_id):    
        if role_id:        
            tasks = TaskModel.query.join(PrivilegeModel, PrivilegeModel.task_id == TaskModel.task_id) \
                            .join(RoleModel, PrivilegeModel.role_id == RoleModel.role_id) \
                            .join(ModuleModel, TaskModel.module_id == ModuleModel.module_id) \
                            .filter(TaskModel.isnavbar == 1) \
                            .filter(ModuleModel.module_id != 1) \
                            .filter(PrivilegeModel.role_id == role_id) \
                            .all()
            # Group tasks by module
            grouped_tasks = {}
            for task in tasks:
                module_title = task.module.module_title  # Access module title
                module_icon = task.module.module_icon 
                if module_title not in grouped_tasks:
                    grouped_tasks[module_title] = {'tasks': [], 'module_icon': module_icon}
                grouped_tasks[module_title]['tasks'].append(task)
            return grouped_tasks
        else:
            return {}  # Handle case where user is not found



class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message="Please, enter your username!")])
    email_address = StringField('Email', validators=[DataRequired(message="Please enter your email address."), Email(message="Please enter a valid Email adddress!")])
    password = PasswordField('Password', validators=[DataRequired(message="Please, enter your password!")])
    lastname = StringField('Last Name', validators=[DataRequired(message="Please, enter your lastname!")])
    firstname = StringField('First Name', validators=[DataRequired(message="Please, enter your firstname!")])
    phonenumber = StringField('Phone Number')
    dateofbirth = StringField('Date of Birth')
    terms = BooleanField('Terms', validators=[DataRequired(message="You must agree before submitting.!")])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username_or_email = StringField('username_or_email', validators=[DataRequired(message="Please, enter your username/email address!")])    
    password = PasswordField('Password', validators=[DataRequired(message="Please, enter your password!")])    
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')    
