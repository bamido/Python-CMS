from app.models.mydb  import db
from sqlalchemy import Enum
from enum import Enum as PyEnum  # Import Enum from Python's enum module
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, ValidationError

# Define the enum class for PageStatus
class PageStatus(PyEnum):
    PUBLISHED = "Published"
    PENDING = "Pending"
    DELETED = "Deleted"


class PageModel(db.Model):
    __tablename__ = 'pages'

    page_id = db.Column(db.Integer, primary_key=True)
    pagetitle = db.Column(db.String(100), unique=True, nullable=False)
    pageslug = db.Column(db.String(100), unique=True, nullable=False)
    parent_id = db.Column(db.Integer, nullable=False, default=0)
    metakeyword = db.Column(db.Text, nullable=True)
    metadesc = db.Column(db.Text, nullable=True)
    pagestatus = db.Column(Enum(PageStatus), nullable=False, default=PageStatus.PUBLISHED)
    sortorder = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Define relationship to other Models
    sections = db.relationship('SectionModel', backref='page', lazy=True)
    sliders = db.relationship('SliderModel', backref='page', lazy=True)

    def __repr__(self):
        return '<PageModel {}>'.format(self.pagetitle)

