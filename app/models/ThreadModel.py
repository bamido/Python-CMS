from app.models.mydb  import db
from sqlalchemy import Enum, func
from enum import Enum as PyEnum  # Import Enum from Python's enum module
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, ValidationError
from app.models.PostModel import PostModel

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

    @staticmethod
    def get_all_threads():
        #retrieve all threads
        threads = ThreadModel.query.all()
        return threads

    def get_threads_with_post_count():
    # Perform a LEFT JOIN between threads and posts and count the posts
        result = db.session.query(
            ThreadModel, 
            func.count(PostModel.post_id).label('post_count')  # Count the number of posts
        ).outerjoin(PostModel, ThreadModel.thread_id == PostModel.thread_id) \
        .group_by(ThreadModel.thread_id).all()
        return result

    def get_thread_posts(id):
        #retrieve thread posts
        posts = PostModel.query.filter_by(thread_id=id)
        return posts


class ThreadForm(FlaskForm):    
    threadname = StringField('thread name', validators=[DataRequired(message="thread name field is required!")])    
    threadstatus = StringField('thread slug', validators=[DataRequired(message="thread status field is required!")])    
    sortorder = StringField('sort order', validators=[DataRequired(message="sort order field is required!")])    
    submit = SubmitField('Submit')  

    def __init__(self, original_title, *args, **kwargs):
        super(ThreadForm, self).__init__(*args, **kwargs)
        self.original_title = original_title

    def validate_threadname(self, threadname):
        if threadname.data != self.original_title:
            thread = ThreadModel.query.filter_by(threadname=threadname.data).first()
            if thread:
                raise ValidationError('thread name already exists.')     
