from app.models.mydb  import db
from sqlalchemy import Enum
from enum import Enum as PyEnum
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, ValidationError

# Define the enum class for PostStatus
class PostStatus(PyEnum):
    Published = "Published"
    Pending = "Pending"
    Deleted = "Deleted"


class PostModel(db.Model):
    __tablename__ = 'posts'

    post_id = db.Column(db.Integer, primary_key=True)
    posttitle = db.Column(db.String(255), unique=True, nullable=False)
    postslug = db.Column(db.String(255), unique=True, nullable=False)    
    thread_id = db.Column(db.Integer, db.ForeignKey('threads.thread_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    postintro = db.Column(db.LargeBinary, nullable=True)
    postbody = db.Column(db.LargeBinary, nullable=False)    
    postimageurl = db.Column(db.String(255), nullable=True)    
    postvideourl = db.Column(db.String(255), nullable=True)    
    poststatus = db.Column(Enum(PostStatus), nullable=False, default=PostStatus.Pending)
    postview = db.Column(db.Integer, nullable=False, default=0)
    sortorder = db.Column(db.Integer, nullable=False, default=0)
    metakeyword = db.Column(db.Text, nullable=True)
    metadesc = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Define relationship to other Models
    posttags = db.relationship('PostTagModel', backref='post', lazy=True)


    def __repr__(self):
        return '<PostModel {}>'.format(self.posttitle)
