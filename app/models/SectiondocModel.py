from app.models.mydb  import db
from sqlalchemy import Enum
from enum import Enum as PyEnum
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, ValidationError

# Define the enum class for SectiondocStatus
class SectiondocStatus(PyEnum):
    PUBLISHED = "Published"
    PENDING = "Pending"
    DELETED = "Deleted"

class DocType(PyEnum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"    
    PDF = "pdf"
    OTHERS = "others"


class SectiondocModel(db.Model):
    __tablename__ = 'sectiondocs'

    sectiondoc_id = db.Column(db.Integer, primary_key=True)    
    section_id = db.Column(db.Integer, db.ForeignKey('sections.section_id'), nullable=False)
    description = db.Column(db.Text, nullable=True)    
    docurl = db.Column(db.String(255), nullable=False)    
    doctype = db.Column(Enum(DocType), nullable=False, default=DocType.IMAGE)
    sectiondocstatus = db.Column(Enum(SectiondocStatus), nullable=False, default=SectiondocStatus.PUBLISHED)
    sortorder = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


    def __repr__(self):
        return '<SectiondocModel {}>'.format(self.sectiondoc_id)


class SectionDocForm(FlaskForm):    
    section_id = StringField('section id', validators=[DataRequired(message="section id field is required!")])
    description = StringField('description')    
    docurl = StringField('docurl')
    doctype = StringField('doctype', validators=[DataRequired(message="doctype field is required!")])    
    sortorder = StringField('sort order', validators=[DataRequired(message="sort order field is required!")])    
    submit = SubmitField('Submit') 