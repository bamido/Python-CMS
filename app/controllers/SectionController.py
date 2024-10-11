from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.models.PageModel import PageModel
from app.models.SectionModel import SectionModel, SectionForm
from app.models.SectiondocModel import SectiondocModel, SectionDocForm
from app.config import Config
from app.models.mydb import db
from flask_login import login_required
from flask_wtf.csrf import generate_csrf
from slugify import slugify
from app.utils import allowed_file, resize_image, create_thumbnail
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.utils import secure_filename
import os
import uuid

bp_section = Blueprint('bp_section', __name__)

@bp_section.route('/sections')
@login_required
def listsections():
    csrf_token = generate_csrf()
    # get all sections
    from app.models.PageModel import PageModel
    allsections = PageModel.get_all_sections()
    
    return render_template('cms/listallsections.html', allsections=allsections, moduletitle="Website(CMS)", title='All Sections', app_name=Config.APP_NAME, author=Config.AUTHOR, csrf_token=csrf_token)


@bp_section.route('/addsection/<int:id>', methods=['GET', 'POST'])
@login_required
def addsection(id):
    page = PageModel.query.get_or_404(id)
    base_url = request.host_url
    form = SectionForm(request.form)
    pages = PageModel.get_all_pages()
    if request.method == 'POST':
        if form.validate():
            try:
                sectiontitle = form.sectiontitle.data
                sectionslug = slugify(form.sectiontitle.data)
                page_id = form.page_id.data
                sectionintro = form.sectionintro.data.encode('utf-8')
                sectionbody = form.sectionbody.data.encode('utf-8')
                sectionicon = form.sectionicon.data
                extlink = form.extlink.data
                sectionstatus = form.sectionstatus.data
                sortorder = form.sortorder.data            
                
                # Create a new SectionModel instance
                newsection = SectionModel(sectiontitle=sectiontitle, sectionslug=sectionslug, page_id=page_id, sectionintro=sectionintro, sectionbody=sectionbody, sectionicon=sectionicon, extlink=extlink, sectionstatus=sectionstatus, sortorder=sortorder)
                # Add the new newsection to the database session
                db.session.add(newsection)
                db.session.flush()  # Flush to get the section_id without committing
                
                # process section image upload
                if 'sectionimage' in request.files:
                    file = request.files['sectionimage']
                    if file and allowed_file(file.filename):
                        # Generate a unique filename using UUID
                        file_extension = file.filename.rsplit('.', 1)[1].lower()
                        unique_filename = str(uuid.uuid4()) + '.' + file_extension

                        # Secure the filename and save it
                        original_path = os.path.join(Config.UPLOAD_PHOTO_DIR, secure_filename(unique_filename))
                        file.save(original_path)

                        # Resize the original image
                        resized_image_path = os.path.join(Config.UPLOAD_PHOTO_DIR, unique_filename)
                        resize_image(original_path, resized_image_path, base_width=800)  # Resize to 800px width

                        # Create a thumbnail
                        thumbnail_path = os.path.join(Config.UPLOAD_PHOTO_DIR, 'thumb_' + unique_filename)
                        create_thumbnail(resized_image_path, thumbnail_path, thumb_size=(450, 450))

                        # insert into sectiondocs table
                        thumbfilename = 'thumb_' + unique_filename
                        newsectiondoc = SectiondocModel(section_id=newsection.section_id, docurl=thumbfilename, doctype='IMAGE', sectiondocstatus='PUBLISHED', sortorder='1')
                        db.session.add(newsectiondoc)
                    
                # Commit changes to the database
                db.session.commit()
                flash('Section added successfully.', 'success')  
                return jsonify({'success':True})

            except SQLAlchemyError as e:
                db.session.rollback()  # Rollback the transaction in case of an error
                #print(f"Error occurred: {str(e)}")
                return jsonify({'errors':str(e)})
            
        else:
            errors = form.errors
            return jsonify({'errors':errors})

    return render_template('cms/addsection.html', form=form, base_url=base_url, pages=pages, id=id)



@bp_section.route('/editsection/<int:id>', methods=['GET', 'POST'])
@login_required
def editsection(id):
    section = SectionModel.query.get_or_404(id)
    base_url = request.host_url
    form = SectionForm(request.form)
    pages = PageModel.get_all_pages()
    form = SectionForm(original_title=section.sectiontitle, obj=section)    
    if request.method == 'POST':
        if form.validate():
            section.sectiontitle = form.sectiontitle.data
            section.sectionslug = slugify(form.sectiontitle.data)
            section.page_id = form.page_id.data
            section.sectionintro = form.sectionintro.data.encode('utf-8')
            section.sectionbody = form.sectionbody.data.encode('utf-8')
            section.sectionicon = form.sectionicon.data
            section.extlink = form.extlink.data
            section.sectionstatus = form.sectionstatus.data
            section.sortorder = form.sortorder.data                        
            # Commit changes to the database
            db.session.commit()
            flash('Section updated successfully.', 'success')            
            return jsonify({'success':True})
        else:
            errors = form.errors
            return jsonify({'errors':errors})

    return render_template('cms/editsection.html', form=form, base_url=base_url, pages=pages, id=id, section=section)


@bp_section.route('/deletesection/<int:id>', methods=['GET', 'DELETE'])
@login_required
def deletesection(id):
    # find section by id
    section = SectionModel.query.get(id)
    if section:
        #db.session.delete(section)
        section.sectionstatus = 'DELETED'
        db.session.commit()
        return jsonify({'message': 'Section deleted successfully'}), 200
    else:
        return jsonify({'message': 'Section not found'}), 404


@bp_section.route('/sectiondocs/<int:id>')
@login_required
def listsectiondocss(id):
    csrf_token = generate_csrf()
    form = SectionDocForm(request.form)
    # get all section docs
    sectiondocs = SectiondocModel.query.filter_by(section_id=id)
    section = SectionModel.query.get(id)
    docnumber = SectiondocModel.query.filter_by(section_id=id).count() + 1;
    
    return render_template('cms/listsectiondocs.html', sectiondocs=sectiondocs, moduletitle="Website(CMS)", title='Section Docs', app_name=Config.APP_NAME, author=Config.AUTHOR, csrf_token=csrf_token, sectionid=id, form=form, section=section, docnumber=docnumber)


@bp_section.route('/addsectiondoc/<int:id>', methods=['GET', 'POST'])
@login_required
def addsectiondoc(id):
    section = SectionModel.query.get_or_404(id)
    base_url = request.host_url
    form = SectionDocForm(request.form)
    if request.method == 'POST':
        print('method is post')
        if form.validate():            
            try:                
                section_id = form.section_id.data                
                doctype = form.doctype.data                
                sortorder = form.sortorder.data 
                description = form.description.data 
                thedocurl =  form.docurl.data       
                
                # process docurl file upload                
                if 'docurl' in request.files:
                    file = request.files['docurl']
                    if file and allowed_file(file.filename):
                        # Generate a unique filename using UUID
                        file_extension = file.filename.rsplit('.', 1)[1].lower()
                        unique_filename = str(uuid.uuid4()) + '.' + file_extension

                        # Secure the filename and save it
                        original_path = os.path.join(Config.UPLOAD_PHOTO_DIR, secure_filename(unique_filename))
                        file.save(original_path)

                        # Resize the original image
                        resized_image_path = os.path.join(Config.UPLOAD_PHOTO_DIR, unique_filename)
                        resize_image(original_path, resized_image_path, base_width=800)  # Resize to 800px width

                        # Create a thumbnail
                        thumbnail_path = os.path.join(Config.UPLOAD_PHOTO_DIR, 'thumb_' + unique_filename)
                        create_thumbnail(resized_image_path, thumbnail_path, thumb_size=(450, 450))

                        # insert into sectiondocs table
                        thumbfilename = 'thumb_' + unique_filename
                        newsectiondoc = SectiondocModel(section_id=section_id, docurl=thumbfilename, doctype=doctype, sectiondocstatus='PUBLISHED', sortorder=sortorder, description=description)
                        db.session.add(newsectiondoc)
                        # Commit changes to the database
                        db.session.commit()
                else:
                    newsectiondoc = SectiondocModel(section_id=section_id, docurl=thedocurl, doctype=doctype, sectiondocstatus='PUBLISHED', sortorder=sortorder, description=description)
                    db.session.add(newsectiondoc)
                    # Commit changes to the database
                    db.session.commit()

                sectiondocs = SectiondocModel.query.filter_by(section_id=id)
                flash('Section documents added successfully.', 'success')  
                return render_template('cms/ajaxsectiondoc.html', form=form, base_url=base_url, sectiondocs=sectiondocs, id=id, section=section)

            except SQLAlchemyError as e:
                db.session.rollback()  # Rollback the transaction in case of an error
                #print(f"Error occurred: {str(e)}")
                return jsonify({'errors':str(e)})
            
        else:
            print("errors")
            errors = form.errors
            return jsonify({'errors':errors})


@bp_section.route('/deletesectiondoc/<int:id>', methods=['GET', 'DELETE', 'POST'])
@login_required
def deletesectiondoc(id):
    # find sectiondoc by id
    sectiondoc = SectiondocModel.query.get(id)
    if sectiondoc:
        db.session.delete(sectiondoc)
        #sectiondoc.sectiondocstatus = 'DELETED'
        db.session.commit()
        return jsonify({'message': 'Section doc deleted successfully', 'success':True}), 200
    else:
        return jsonify({'message': 'Section doc not found'}), 404
