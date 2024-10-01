from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.models.ModuleModel import ModuleModel, ModuleForm
from app.config import Config
from app.models.mydb import db
from flask_login import login_required
from flask_wtf.csrf import generate_csrf

bp_module = Blueprint('bp_module', __name__)

@bp_module.route('/modules')
@login_required
def listmodules():
    csrf_token = generate_csrf()
    modules = ModuleModel.get_all_modules()
    return render_template('rbac/listmodules.html', modules=modules, moduletitle="Access Control", title='Modules', app_name=Config.APP_NAME, author=Config.AUTHOR, csrf_token=csrf_token)


@bp_module.route('/addmodule', methods=['GET', 'POST'])
@login_required
def addmodule():
    base_url = request.host_url
    form = ModuleForm(request.form)
    if request.method == 'POST':
        if form.validate():
            module_title = form.module_title.data
            module_order = form.module_order.data
            module_icon = form.module_icon.data
            # Create a new ModuleModel instance
            newmodule = ModuleModel(module_title=module_title, module_order=module_order, module_icon=module_icon)
            # Add the new module to the database session
            db.session.add(newmodule)
            # Commit changes to the database
            db.session.commit()
            flash('Module added successfully.', 'success')  
            #return redirect(url_for('bp_module.listmodules'))            
            return jsonify({'success':True})
        else:
            errors = form.errors
            return jsonify({'errors':errors})
    return render_template('rbac/addmodule.html', form=form, base_url=base_url)            


@bp_module.route('/editmodule/<int:id>', methods=['GET', 'POST'])
@login_required
def editmodule(id):
    module = ModuleModel.query.get_or_404(id)
    base_url = request.host_url
    form = ModuleForm(original_title=module.module_title, obj=module)
    if request.method == 'POST':
        if form.validate():
            module.module_title = form.module_title.data
            module.module_order = form.module_order.data
            module.module_icon = form.module_icon.data                        
            # Commit changes to the database
            db.session.commit()
            flash('Module updated successfully.', 'success')            
            return jsonify({'success':True})
        else:
            errors = form.errors
            return jsonify({'errors':errors})
    return render_template('rbac/editmodule.html', form=form, module=module, base_url=base_url)
    

@bp_module.route('/deletemodule/<int:id>', methods=['GET','DELETE'])
def deletemodule(id):
    # Find the module record by ID
    module = ModuleModel.query.get(id)
    if module:
        # Delete the module record from the database session
        db.session.delete(module)
        # Commit the session to permanently delete the record from the database
        db.session.commit()
        flash('Module deleted successfully.', 'success')            
        return jsonify({'message': 'Module deleted successfully'}), 200
    else:
        return jsonify({'message': 'Module not found'}), 404

