from app.models.mydb  import db
from sqlalchemy import Enum
from enum import Enum as PyEnum
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Optional

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

    def get_sliders():
        sliders = SliderModel.query.all()
        return sliders

    


class SliderForm(FlaskForm):    
    title = StringField('title', validators=[DataRequired(message="slider title field is required!")])
    page_id = IntegerField('page id', validators=[DataRequired(message="page id field is required!")])
    subtitle = StringField('subtitle')    
    body = StringField('body')
    imageurl = StringField('image url')
    link1 = StringField('link1')    
    link2 = StringField('link2')
    sliderstatus = StringField('slider status', validators=[DataRequired(message="slider status field is required!")])    
    align = StringField('align', validators=[DataRequired(message="align field is required!")])    
    sortorder = StringField('sort order', validators=[DataRequired(message="sort order field is required!")])    
    submit = SubmitField('Submit')  

    def __init__(self, original_title=None, original_page_id=None, original_imageurl=None, is_update=False, *args, **kwargs):
        super(SliderForm, self).__init__(*args, **kwargs)
        self.original_title = original_title
        self.original_page_id = original_page_id

        # Conditionally add validators based on insert/update mode
        if is_update:
            # If it's an update, the image is not required (use Optional)
            self.imageurl.validators = [Optional()]
        else:
            # If it's a new record (insert), the image is required
            self.imageurl.validators = [DataRequired(message="Image field is required!")]

        self.original_imageurl = original_imageurl

    def validate_title(self, title):
        # Only check for duplicates if the title or page_id has changed
        if title.data != self.original_title or self.page_id.data != self.original_page_id:
            # Query the database for an existing slider with the same title and page_id
            slider = SliderModel.query.filter_by(title=title.data, page_id=self.page_id.data).first()
            # Make sure we're not comparing with the same record            
            print(self.original_title)
            if slider and slider.title != self.original_title:
                raise ValidationError('Slider title already exists for this page.')
