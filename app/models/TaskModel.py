from app.models.mydb import db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, ValidationError

class TaskModel(db.Model):
    __tablename__ = 'tasks'

    task_id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.module_id'), nullable=False)
    task_label = db.Column(db.String(100), nullable=False)
    task_url = db.Column(db.String(100))
    task_route = db.Column(db.String(100))
    task_method = db.Column(db.String(100))
    task_icon = db.Column(db.String(50))
    isdashboard = db.Column(db.Boolean, default=False)
    isnavbar = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    privileges = db.relationship('PrivilegeModel', backref='task', lazy=True)

    def __repr__(self):
        return '<TaskModel {}>'.format(self.task_id)

    def get_all_tasks():
        result = TaskModel.query.all()
        return result

class TaskForm(FlaskForm):    
    module_id = StringField('module title', validators=[DataRequired(message="module title field is required!")])
    task_label = StringField('task label', validators=[DataRequired(message="task label field is required!")])
    task_url = StringField('task url', validators=[DataRequired(message="task url field is required!")])    
    task_route = StringField('task route', validators=[DataRequired(message="task route field is required!")])
    task_method = StringField('task method', validators=[DataRequired(message="task method field is required!")])    
    task_label = StringField('task label', validators=[DataRequired(message="task label field is required!")])
    task_icon = StringField('task icon')
    isdashboard = StringField('isdashboard', validators=[DataRequired(message="isdashboard field is required!")])    
    isnavbar = StringField('isnavbar', validators=[DataRequired(message="isnavbar field is required!")])    
    submit = SubmitField('Submit')   

    def __init__(self, original_title, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.original_title = original_title

    def validate_task_route(self, task_route):
        if task_route.data != self.original_title:
            task = TaskModel.query.filter_by(task_route=task_route.data).first()
            if task:
                raise ValidationError('task route already exists.')     
