from app.models.mydb  import db
from sqlalchemy import Enum
from enum import Enum as PyEnum  # Import Enum from Python's enum module
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, ValidationError

# Define the enum class for ThreadStatus
class ThreadStatus(PyEnum):
    Published = "Published"
    Pending = "Pending"
    Deleted = "Deleted"


class ThreadModel(db.Model):
    __tablename__ = 'threads'

    thread_id = db.Column(db.Integer, primary_key=True)
    threadname = db.Column(db.String(255), unique=True, nullable=False)
    threadslug = db.Column(db.String(255), unique=True, nullable=False)
    threadstatus = db.Column(Enum(ThreadStatus), nullable=False, default=ThreadStatus.Published)
    sortorder = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Define relationship to other Models
    posts = db.relationship('PostModel', backref='thread', lazy=True)

    def __repr__(self):
        return '<ThreadModel {}>'.format(self.threadname)

