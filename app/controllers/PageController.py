from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.models.PageModel import PageModel, PageForm
from app.models.SectionModel import SectionModel
from app.config import Config
from app.models.mydb import db
from flask_login import login_required
from flask_wtf.csrf import generate_csrf
from slugify import slugify

bp_page = Blueprint('bp_page', __name__)

@bp_page.route('/pages')
@login_required
def listpages():
    csrf_token = generate_csrf()
    # get all pages
    pages = PageModel.get_pages_with_section_count()
    
    return render_template('cms/listpages.html', pages=pages, moduletitle="Website(CMS)", title='Pages', app_name=Config.APP_NAME, author=Config.AUTHOR, csrf_token=csrf_token)


@bp_page.route('/addpage', methods=['GET', 'POST'])
@login_required
def addpage():
    base_url = request.host_url
    form = PageForm(request.form)
    pages = PageModel.get_all_pages()
    if request.method == 'POST':
        if form.validate():
            pagetitle = form.pagetitle.data
            pageslug = slugify(form.pagetitle.data)
            parent_id = form.parent_id.data
            metakeyword = form.metakeyword.data
            metadesc = form.metadesc.data
            pagestatus = form.pagestatus.data
            sortorder = form.sortorder.data
            
            # Create a new PageModel instance
            newpage = PageModel(pagetitle=pagetitle, pageslug=pageslug, parent_id=parent_id, pagestatus=pagestatus, sortorder=sortorder, metakeyword=metakeyword, metadesc=metadesc)
            # Add the new page to the database session
            db.session.add(newpage)
            # Commit changes to the database
            db.session.commit()
            flash('Page added successfully.', 'success')  
            return jsonify({'success':True})
        else:
            errors = form.errors
            return jsonify({'errors':errors})

    return render_template('cms/addpage.html', form=form, base_url=base_url, pages=pages)

@bp_page.route('/editpage/<int:id>', methods=['GET', 'POST'])
@login_required
def editpage(id):
    page = PageModel.query.get_or_404(id)
    base_url = request.host_url
    pages = PageModel.get_all_pages()
    form = PageForm(original_title=page.pagetitle, obj=page)    
    if request.method == 'POST':
        if form.validate():
            page.pagetitle = form.pagetitle.data
            page.pageslug = slugify(form.pagetitle.data)
            page.parent_id = form.parent_id.data
            page.metakeyword = form.metakeyword.data
            page.metadesc = form.metadesc.data
            page.pagestatus = form.pagestatus.data
            page.sortorder = form.sortorder.data                       
            # Commit changes to the database
            db.session.commit()
            flash('Page updated successfully.', 'success')            
            return jsonify({'success':True})
        else:
            errors = form.errors
            return jsonify({'errors':errors})
    return render_template('cms/editpage.html', pages=pages, form=form, page=page, base_url=base_url)


@bp_page.route('/deletepage/<int:id>', methods=['GET', 'DELETE'])
@login_required
def deletepage(id):
    # find page by id
    page = PageModel.query.get(id)
    if page:
        #db.session.delete(page)
        page.pagestatus = 'DELETED'
        db.session.commit()
        return jsonify({'message': 'Page deleted successfully'}), 200
    else:
        return jsonify({'message': 'Page not found'}), 404



@bp_page.route('/pagesections/<int:id>', methods=['GET'])
@login_required
def listpagesections(id):
    csrf_token = generate_csrf()
    # get page sections
    pagesections = PageModel.get_page_sections(id)
    page = PageModel.query.get(id)
    title = page.pagetitle + ' Page Sections'

    return render_template('cms/listsections.html', pagesections=pagesections, moduletitle="Website(CMS)", title=title, app_name=Config.APP_NAME, author=Config.AUTHOR, csrf_token=csrf_token, id=id, page=page)
