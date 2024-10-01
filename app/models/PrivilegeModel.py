from app.models.mydb import db
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, FieldList, BooleanField
from wtforms.validators import DataRequired, Email, ValidationError

class PrivilegeModel(db.Model):
    __tablename__ = 'privileges'

    privilege_id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.task_id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'), nullable=False)
    created_at = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


    def __repr__(self):
        return '<PrivilegeModel {}>'.format(self.privilege_id)


class PrivilegeForm(FlaskForm):    
    task_id = FieldList(IntegerField('task id'))    
    #task_id = IntegerField('role id', validators=[DataRequired(message="role id field is required!")])    
    role_id = IntegerField('role id', validators=[DataRequired(message="role id field is required!")])    
    submit = SubmitField('Submit')         