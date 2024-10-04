from app.models.mydb  import db
from sqlalchemy import Enum
from enum import Enum as PyEnum
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, ValidationError

# Define the enum class for SliderStatus
class SliderStatus(PyEnum):
    Published = "Published"
    Pending = "Pending"
    Deleted = "Deleted"

class SliderAlign(PyEnum):
    Left = "Left"
    Center = "Center"
    Right = "Right"


class SliderModel(db.Model):
    __tablename__ = 'sliders'

    slider_id = db.Column(db.Integer, primary_key=True)
    page_id = db.Column(db.Integer, db.ForeignKey('pages.page_id'), nullable=False)    
    title = db.Column(db.String(255), nullable=False)
    subtitle = db.Column(db.String(255), nullable=True)        
    body = db.Column(db.LargeBinary, nullable=True)
    imageurl = db.Column(db.String(255), nullable=False)
    link1 = db.Column(db.String(255), nullable=True)
    link2 = db.Column(db.String(255), nullable=True)    
    sliderstatus = db.Column(Enum(SliderStatus), nullable=False, default=SliderStatus.Published)
    align = db.Column(Enum(SliderAlign), nullable=False, default=SliderAlign.Left)
    sortorder = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return '<SliderModel {}>'.format(self.title)
