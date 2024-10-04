from app.models.mydb  import db
from sqlalchemy import Enum
from enum import Enum as PyEnum
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, ValidationError

# Define the enum class for Status
class Status(PyEnum):
    Published = "Published"
    Pending = "Pending"
    Deleted = "Deleted"

class TestimonialModel(db.Model):
    __tablename__ = 'testimonials'

    testimonial_id = db.Column(db.Integer, primary_key=True)    
    fullname = db.Column(db.String(255), nullable=False)    
    body = db.Column(db.LargeBinary, nullable=False)
    company = db.Column(db.String(255), nullable=True)
    imageurl = db.Column(db.String(255), nullable=True)    
    status = db.Column(Enum(Status), nullable=False, default=Status.Pending)
    sortorder = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return '<TestimonialModel {}>'.format(self.fullname)
