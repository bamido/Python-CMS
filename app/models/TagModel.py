from app.models.mydb  import db
from sqlalchemy import Enum
from enum import Enum as PyEnum  # Import Enum from Python's enum module
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, ValidationError

class TagModel(db.Model):
    __tablename__ = 'tags'

    tag_id = db.Column(db.Integer, primary_key=True)
    tagname = db.Column(db.String(255), unique=True, nullable=False)
    tagslug = db.Column(db.String(255), unique=True, nullable=False)    
    created_at = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Define relationship to other Models
    posttags = db.relationship('PostTagModel', backref='tag', lazy=True)

    def __repr__(self):
        return '<TagModel {}>'.format(self.tagname)

