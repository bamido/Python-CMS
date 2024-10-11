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

    @staticmethod
    def get_all_sections():
        # get all sections by join pages and sections
        result = db.session.query(
            PageModel,
            SectionModel
        ).outterjoin(SectionModel, PageModel.page_id == SectiondocModel.page_id) \
        .all()
        return result


class SectionForm(FlaskForm):    
    sectiontitle = StringField('section title', validators=[DataRequired(message="section title field is required!")])
    page_id = StringField('page name', validators=[DataRequired(message="page name field is required!")])
    sectionintro = StringField('section intro')    
    sectionbody = StringField('section body', validators=[DataRequired(message="section body field is required!")])
    sectionicon = StringField('section icon')
    extlink = StringField('al linkextern')
    sectionstatus = StringField('section status', validators=[DataRequired(message="section status field is required!")])    
    sortorder = StringField('sort order', validators=[DataRequired(message="sort order field is required!")])    
    submit = SubmitField('Submit') 

    def __init__(self, original_title, *args, **kwargs):
        super(SectionForm, self).__init__(*args, **kwargs)
        self.original_title = original_title

    def validate_sectiontitle(self, sectiontitle):
        if sectiontitle.data != self.original_title:
            section = SectionModel.query.filter_by(sectiontitle=sectiontitle.data).first()
            if section:
                raise ValidationError('section title already exists.')



# class SectionForm(FlaskForm):    
#     section_id = StringField('section title', validators=[DataRequired(message="section title field is required!")])
#     page_id = StringField('page name', validators=[DataRequired(message="page name field is required!")])
#     sectionintro = StringField('section intro')    
#     sectionbody = StringField('section body', validators=[DataRequired(message="section body field is required!")])
#     sectionicon = StringField('section icon')
#     extlink = StringField('al linkextern')
#     sectionstatus = StringField('section status', validators=[DataRequired(message="section status field is required!")])    
#     sortorder = StringField('sort order', validators=[DataRequired(message="sort order field is required!")])    
#     submit = SubmitField('Submit')  