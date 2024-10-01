from app.models.mydb import db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, ValidationError, Optional
from app.models.uniquefield import Unique

class ModuleModel(db.Model):
    __tablename__ = 'modules'

    module_id = db.Column(db.Integer, primary_key=True)
    module_title = db.Column(db.String(100), unique=True, nullable=False)
    module_order = db.Column(db.Integer, nullable=False)
    module_icon = db.Column(db.String(50))
    created_at = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    tasks = db.relationship('TaskModel', backref='module', lazy=True)

    def __repr__(self):
        return '<ModuleModel {}>'.format(self.module_title)

    def get_all_modules():
        result = ModuleModel.query.all()
        return result

class ModuleForm(FlaskForm):    
    module_title = StringField('module title', validators=[DataRequired(message="module title field is required!")])
    module_order = StringField('module order', validators=[DataRequired(message="module order field is required!")])
    module_icon = StringField('module icon', validators=[DataRequired(message="module icon field is required!")])    
    submit = SubmitField('Submit')   

    def __init__(self, original_title, *args, **kwargs):
        super(ModuleForm, self).__init__(*args, **kwargs)
        self.original_title = original_title

    def validate_module_title(self, module_title):
        if module_title.data != self.original_title:
            module = ModuleModel.query.filter_by(module_title=module_title.data).first()
            if module:
                raise ValidationError('module title already exists.')             