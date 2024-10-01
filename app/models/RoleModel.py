from sqlalchemy import Enum
from app.models.mydb import db
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, ValidationError

class RoleStatus(Enum):
    PUBLISHED = "Published"
    PENDING = "Pending"
    DELETED = "Deleted"

class RoleModel(db.Model):
    __tablename__ = 'roles'

    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    #rolestatus = db.Column(Enum(RoleStatus), nullable=False, server_default=RoleStatus.PENDING)

    users = db.relationship('UserModel', backref='role', lazy=True)
    privileges = db.relationship('PrivilegeModel', backref='role', lazy=True)

    def __repr__(self):
        return '<RoleModel {}>'.format(self.role_name)

    @staticmethod
    def get_all_roles():
        #retrieve all roles
        roles = RoleModel.query.all()
        return roles

class RoleForm(FlaskForm):    
    role_name = StringField('role name', validators=[DataRequired(message="role name field is required!")])    
    submit = SubmitField('Submit')   

    def __init__(self, original_title, *args, **kwargs):
        super(RoleForm, self).__init__(*args, **kwargs)
        self.original_title = original_title

    def validate_role_name(self, role_name):
        if role_name.data != self.original_title:
            role = RoleModel.query.filter_by(role_name=role_name.data).first()
            if role:
                raise ValidationError('role name already exists.')     
