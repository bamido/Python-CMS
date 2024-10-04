from app.models.mydb  import db
from sqlalchemy import Enum
from enum import Enum as PyEnum
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, ValidationError

# Define the enum class for SectionStatus
class SectionStatus(PyEnum):
    PUBLISHED = "Published"
    PENDING = "Pending"
    DELETED = "Deleted"


class SectionModel(db.Model):
    __tablename__ = 'sections'

    section_id = db.Column(db.Integer, primary_key=True)
    sectiontitle = db.Column(db.String(255), unique=True, nullable=False)
    sectionslug = db.Column(db.String(255), unique=True, nullable=False)    
    page_id = db.Column(db.Integer, db.ForeignKey('pages.page_id'), nullable=False)
    sectionintro = db.Column(db.LargeBinary, nullable=True)
    sectionbody = db.Column(db.LargeBinary, nullable=False)
    sectionicon = db.Column(db.String(100), nullable=True)
    extlink = db.Column(db.String(255), nullable=True)
    sectionstatus = db.Column(Enum(SectionStatus), nullable=False, default=SectionStatus.PUBLISHED)
    sortorder = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Define relationship to other Models
    sectiondocs = db.relationship('SectiondocModel', backref='section', lazy=True)


    def __repr__(self):
        return '<SectionModel {}>'.format(self.sectiontitle)
