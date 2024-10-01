from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.models.RoleModel import RoleModel, RoleForm
from app.models.ModuleModel import ModuleModel
from app.models.PrivilegeModel import PrivilegeModel, PrivilegeForm
from app.config import Config
from app.models.mydb import db
from flask_login import login_required
from flask_wtf.csrf import generate_csrf

bp_role = Blueprint('bp_role', __name__)

@bp_role.route('/roles')
@login_required
def listroles():
    csrf_token = generate_csrf()
    #retrieve all roles
    roles = RoleModel.get_all_roles()
    return render_template('rbac/listroles.html', roles=roles, moduletitle="Access Control", title='Roles', app_name=Config.APP_NAME, author=Config.AUTHOR, csrf_token=csrf_token)

@bp_role.route('/addrole', methods=['GET', 'POST'])
@login_required
def addrole():
    base_url = request.host_url
    form = RoleForm(request.form)
    if request.method == 'POST':
        if form.validate():
            rolename = form.role_name.data

            newrole = RoleModel(role_name=rolename)
            db.session.add(newrole)
            db.session.commit()
            flash('Role added successfully.', 'success')  
            return jsonify({'success':True})
        else:
            errors = form.errors
            return jsonify({'errors':errors})

    return render_template('rbac/addrole.html', form=form, base_url=base_url)


@bp_role.route('/editrole/<int:id>', methods=['GET','POST'])
@login_required
def editrole(id):
    role = RoleModel.query.get_or_404(id)
    base_url = request.host_url
    form = RoleForm(request.form)
    if request.method == 'POST':
        if form.validate():
            role.role_name = form.role_name.data
            # Commit changes to the database
            db.session.commit()
            flash('Role updated successfully.', 'success')            
            return jsonify({'success':True})
        else:
            errors = form.errors
            return jsonify({'errors':errors})
    return render_template('rbac/editrole.html', form=form, role=role, base_url=base_url)


@bp_role.route('/deleterole/<int:id>', methods=['GET','DELETE'])
def deleterole(id):
    # Find the role record by ID
    role = RoleModel.query.get(id)
    if role:
        # Delete the role record from the database session
        db.session.delete(role)
        # Commit the session to permanently delete the record from the database
        db.session.commit()
        return jsonify({'message': 'Role deleted successfully'}), 200
    else:
        return jsonify({'message': 'Role not found'}), 404


@bp_role.route('/assignprivileges/<int:id>', methods=['GET', 'POST'])
@login_required
def assignprivileges(id):
    role = RoleModel.query.get(id)
    modules = ModuleModel.get_all_modules()
    role_privileges = [p.task_id for p in role.privileges]  # Extract task IDs from privileges
    #print(role_privileges)    
    form = PrivilegeForm(request.form)
    assign_url = url_for('bp_role.assignprivileges', id=id)  # Generate URL with id param
    if request.method == 'POST':
        if form.validate_on_submit():
            roleid = form.role_id.data
            taskids = request.form.getlist('task_id[]')
            '''print(f"form.data: {form.data}")  # Print all form data
            print(f"form.task_id.data: {form.task_id.data}")  # Print specific field data
            print(f"roleid: {roleid}")
            print(f"taskids: {taskids}")
            print('Weldone!')'''
            privileges = []
            if taskids:  # Check if taskids is not None before iterating
                
                # Delete existing privileges for this role
                db.session.query(PrivilegeModel).filter_by(role_id=roleid).delete()
                db.session.commit()

                for taskid in taskids:
                    privilege = PrivilegeModel(task_id=taskid, role_id=roleid)
                    privileges.append(privilege)
                # Add all privileges to the database session
                db.session.add_all(privileges)
                db.session.commit()
                flash('Privileges assigned successfully.', 'success')            
                role_privileges = [p.task_id for p in role.privileges]  # Extract task IDs from privileges
                return render_template('rbac/assignprivleges.html', moduletitle='Access Control', title='Assign Privileges', role=role, modules=modules, id=id, form=form, assign_url=assign_url, role_privileges=role_privileges)
            else:
                flash('No task selected.', 'error')
        else:
            errors = form.errors
            return jsonify({'errors':errors})


    return render_template('rbac/assignprivleges.html', moduletitle='Access Control', title='Assign Privileges', role=role, modules=modules, id=id, form=form, assign_url=assign_url, role_privileges=role_privileges)
