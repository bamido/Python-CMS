from app.models.mydb  import db
from sqlalchemy import Enum
from enum import Enum as PyEnum
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Optional

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

    def get_posts():
        posts = PostModel.query.all()
        return posts



class PostForm(FlaskForm):    
    posttitle = StringField('post title', validators=[DataRequired(message="post title field is required!")])
    thread_id = IntegerField('thread id', validators=[DataRequired(message="thread id field is required!")])
    postintro = StringField('post intro')        
    postbody = StringField('post body', validators=[DataRequired(message="post body field is required!")])
    imageurl = StringField('image url', validators=[DataRequired(message="post image field is required!")])
    postvideourl = StringField('post video url') 
    poststatus = StringField('post status', validators=[DataRequired(message="post status field is required!")])    
    postview = StringField('post view')     
    sortorder = StringField('sort order', validators=[DataRequired(message="sort order field is required!")])    
    metakeyword = StringField('metakeyword') 
    metadesc = StringField('metadesc') 
    submit = SubmitField('Submit')  

    def __init__(self, original_title=None, original_thread_id=None, original_imageurl=None, is_update=False, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.original_title = original_title
        self.original_thread_id = original_thread_id

        # Conditionally add validators based on insert/update mode
        if is_update:
            # If it's an update, the image is not required (use Optional)
            self.imageurl.validators = [Optional()]
        else:
            # If it's a new record (insert), the image is required
            self.imageurl.validators = [DataRequired(message="Image field is required!")]

        self.original_imageurl = original_imageurl

    def validate_posttitle(self, posttitle):
        # Only check for duplicates if the title or thread_id has changed
        if posttitle.data != self.original_title or self.thread_id.data != self.original_thread_id:
            # Query the database for an existing post with the same title and thread_id
            post = PostModel.query.filter_by(posttitle=posttitle.data, thread_id=self.thread_id.data).first()
            # Make sure we're not comparing with the same record            
            print(self.original_title)
            if post and post.posttitle != self.original_title:
                raise ValidationError('Post title already exists for this thread.')

