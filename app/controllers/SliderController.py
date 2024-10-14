from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.models.PageModel import PageModel
from app.models.SliderModel import SliderModel, SliderForm
from app.config import Config
from app.models.mydb import db
from flask_login import login_required
from flask_wtf.csrf import generate_csrf
from app.utils import allowed_file, resize_image, create_thumbnail
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.utils import secure_filename
import os
import uuid


bp_slider = Blueprint('bp_slider', __name__)

@bp_slider.route('/sliders')
@login_required
def listsliders():
    csrf_token = generate_csrf()
    # get all sliders
    sliders = SliderModel.get_sliders()
    return render_template('cms/listsliders.html', sliders=sliders, moduletitle="Website(CMS)", title='Sliders', app_name=Config.APP_NAME, author=Config.AUTHOR, csrf_token=csrf_token)

@bp_slider.route('/addslider', methods=['GET', 'POST'])
@login_required
def addslider():
    base_url = request.host_url
    form = SliderForm(request.form)
    pages = PageModel.get_all_pages()
    if request.method == 'POST':
        if form.validate():
            page_id = form.page_id.data            
            title = form.title.data
            subtitle = form.subtitle.data
            body = form.body.data.encode('utf-8')
            imageurl = form.imageurl.data
            link1 = form.link1.data
            link2 = form.link2.data
            sliderstatus = form.sliderstatus.data
            align = form.align.data
            sortorder = form.sortorder.data
            
            # process section image upload
            if 'imageurl' in request.files:
                file = request.files['imageurl']
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
            
                    # Create a new SliderModel instance
                    thumbfilename = 'thumb_' + unique_filename
                    newslider = SliderModel(page_id=page_id, title=title, subtitle=subtitle, body=body, imageurl=thumbfilename, link1=link1, link2=link2, sliderstatus=sliderstatus, align=align, sortorder=sortorder)
                    # Add the new slider to the database session
                    db.session.add(newslider)
                    # Commit changes to the database
                    db.session.commit()
                    flash('Slide added successfully.', 'success')  
                    return jsonify({'success':True})
        else:
            errors = form.errors
            return jsonify({'errors':errors})

    return render_template('cms/addslider.html', form=form, base_url=base_url, pages=pages)


@bp_slider.route('/editslider/<int:id>', methods=['GET', 'POST'])
@login_required
def editslider(id):
    base_url = request.host_url    
    pages = PageModel.get_all_pages()
    slider = SliderModel.query.get(id)
    form = SliderForm(original_title=slider.title, original_page_id=slider.page_id, original_imageurl=slider.imageurl, is_update=True, formdata=request.form)
    if request.method == 'POST':
        if form.validate():
            
            # If validation passes, update the slider with the new values
            slider.page_id = form.page_id.data            
            slider.title = form.title.data
            slider.subtitle = form.subtitle.data
            slider.body = form.body.data.encode('utf-8')
            # slider.imageurl = form.imageurl.data
            slider.link1 = form.link1.data
            slider.link2 = form.link2.data
            slider.sliderstatus = form.sliderstatus.data
            slider.align = form.align.data
            slider.sortorder = form.sortorder.data

            # process slide image upload
            if 'imageurl' in request.files and request.files['imageurl'].filename:
                file = request.files['imageurl']
                if file and allowed_file(file.filename):
                    # Remove the existing image if it exists
                    existing_image_path = os.path.join(Config.UPLOAD_PHOTO_DIR, slider.imageurl.replace("thumb_", ""))
                    existing_thumbnail_path = os.path.join(Config.UPLOAD_PHOTO_DIR, slider.imageurl)                    
                    # Delete the old image
                    if os.path.exists(existing_image_path):
                        os.remove(existing_image_path)  
                    if os.path.exists(existing_thumbnail_path):
                        os.remove(existing_thumbnail_path)
                                        
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
            
                    # new imageurl
                    slider.imageurl = 'thumb_' + unique_filename                    
                    # Commit changes to the database                                          
                    db.session.commit()
                     
                    flash('Slide updated successfully.', 'success')  
                    return jsonify({'success':True})
            else:
                db.session.commit()
                flash('Slide updated successfully.', 'success')  
                return jsonify({'success':True})
        else:                  
            errors = form.errors
            return jsonify({'errors':errors})

    return render_template('cms/editslider.html', form=form, base_url=base_url, pages=pages, slider=slider)


@bp_slider.route('/deleteslider/<int:id>', methods=['GET', 'DELETE'])
def deleteslider(id):
    # find slide by id
    slider = SliderModel.query.get(id)
    if slider:
        #db.session.delete(slider)
        slider.sliderstatus = 'Deleted'
        db.session.commit()
        return jsonify({'message': 'Slide deleted successfully'}), 200
    else:
        return jsonify({'message': 'Slide not found'}), 404


