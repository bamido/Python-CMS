from app.models.mydb  import db
from sqlalchemy import Enum, func
from enum import Enum as PyEnum  # Import Enum from Python's enum module
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, ValidationError
from app.models.SectionModel import SectionModel

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

    @staticmethod
    def get_all_pages():
        #retrieve all pages
        pages = PageModel.query.all()
        return pages

    def get_pages_with_section_count():
    # Perform a LEFT JOIN between Pages and Sections and count the sections
        result = db.session.query(
            PageModel, 
            func.count(SectionModel.section_id).label('section_count')  # Count the number of sections
        ).outerjoin(SectionModel, PageModel.page_id == SectionModel.page_id) \
        .group_by(PageModel.page_id).all()
        return result

    def get_all_sections():
        # get all sections by join pages and sections
        result = []
        sections = db.session.query(
            PageModel,
            SectionModel
        ).outerjoin(PageModel, SectionModel.page_id == PageModel.page_id) \
        .all()

        from app.models.SectiondocModel import SectiondocModel
        for page, section in sections:
            image = db.session.query(SectiondocModel.docurl) \
                .filter(SectiondocModel.section_id == section.section_id) \
                .filter(SectiondocModel.doctype == 'IMAGE') \
                .first()  # Fetch only the first image
            
          
            result.append({
                'page': page,
                'section': section,
                'docurl': image.docurl if image else None
            })

        return result

    def get_page_sections(id):
        #retrieve specific page sections
        #sections = SectionModel.query.filter_by(page_id=id)
        #return sections

        result = []
        sections = SectionModel.query.filter_by(page_id=id)
        
        from app.models.SectiondocModel import SectiondocModel
        for section in sections:
            image = db.session.query(SectiondocModel.docurl) \
                .filter(SectiondocModel.section_id == section.section_id) \
                .filter(SectiondocModel.doctype == 'IMAGE') \
                .first()  # Fetch only the first image

            result.append({                
                'section': section,
                'docurl': image.docurl if image else None
            })

        return result




class PageForm(FlaskForm):    
    pagetitle = StringField('page title', validators=[DataRequired(message="page title field is required!")])
    parent_id = StringField('parent id', validators=[DataRequired(message="parent id field is required!")])
    metakeyword = StringField('meta keyword')    
    metadesc = StringField('meta description')
    pagestatus = StringField('page status', validators=[DataRequired(message="page status field is required!")])    
    sortorder = StringField('sort order', validators=[DataRequired(message="sort order field is required!")])    
    submit = SubmitField('Submit')  

    def __init__(self, original_title, *args, **kwargs):
        super(PageForm, self).__init__(*args, **kwargs)
        self.original_title = original_title

    def validate_pagetitle(self, pagetitle):
        if pagetitle.data != self.original_title:
            page = PageModel.query.filter_by(pagetitle=pagetitle.data).first()
            if page:
                raise ValidationError('page title already exists.')     
