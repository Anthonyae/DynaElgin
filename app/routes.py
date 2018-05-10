# routes different URL's that the application uses
# python functions are called view functions and are handlers for the application routes

from app import app, db  # importing db to call sql alchemy to query database
from app.forms import LoginForm, RegistrationForm, JobDetailsForm, JobProductionForm, BoxScanForm
from flask import render_template, flash, redirect, url_for, request
# import the User class to validate logged in state 
from app.models import User, Post
# used to check state of user.
# current_user - variable, can be used anytime to obtain the user object that represents the client of the request.
    # the value of the variable can be 1. a user object from database(flask-login reads, called through user loader function)
    # 2. a special anonymous user object if user is not logged in. 
    # 
from flask_login import current_user, login_user, logout_user, login_required
# REREAD THIS
# To determine if the URL is relative or absolue, parse it with url_parse function and then check if the netloc component is set or not.
from werkzeug.urls import url_parse
# testing to use func expression
from sqlalchemy.sql.expression import func
# import from tables.py the class that contains the view of the records that will be pulled
from app.tables import Results, OpenJobs
from datetime import datetime


@app.route('/')
@app.route('/index')
@login_required
# this is a view function
def index():
    posts = {"Pending": ["Mixed part entries", "Showing timestamps in tables",  ]}
    # render_template function takes a template filename and a variable list of template arguments and returns the same template, 
    # but with all the placeholders in it replaced with actual values
    return render_template('index.html', posts=posts)


@app.route('/login', methods=['Get', 'Post'])
def login():
    # Stops user from clicking the log in URL if they are already authenticated.
    if current_user.is_authenticated:  # is_authenticated - to check if user is logged in or not. 
        return redirect(url_for('index'))
    # LoginForm() is from forms.py /User created
    form = LoginForm()
    # form.validate_on_submit() - gathers data, run's all validators attached to fields, and if everything is ok returns TRUE.
    # Otherwise the method returns FALSE, and will cause form to render back to user through "GET" request.
        # When the function form.v_o_s() returns TRUE, the view function calls two new functions imported from Flask. 
            # flash() - way to show a message to the user. #Needs to be called in HTML (here we use base.html) to render. 
            # redirect() - Instructs the client web browser to automatically navigate to a diffrent page, given as an argument.
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("invalid username or password")
            return redirect(url_for('login'))
        # CAN SET SESSION VARIABLES HERE FOR USERS
        # login_user() - registers the user as logged in, future pages the user navigates to will have the current_user variable set to that user.
        login_user(user, remember=form.remember_me.data)  # logs in user and checks remember_me status
        # afer the user is logged in by calling login_user() funciton, the value of the 'next' query string argument  is obtained.
        # requst variable - contains all the information that the client sent with the request.
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash("You have been successfully logged out!")
    return redirect(url_for('index'))


@app.route('/register', methods=['Get', 'Post'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Saving the password even though were saving the password under password_hash as well
        user = User(username=form.username.data, email=form.email.data, temppassword=form.password.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Thank you. You are now a registered user!")
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


# This-> <> indicates dynamic component. Flask will accept anything here and invoke the view function with text as argument.
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'Status': 'open', 'PN': 9220341, 'Job': 324610 }
    ]
    return render_template('user.html', user=user, posts=posts)



@app.route('/Production and Open jobs', methods=['Get', 'Post'])
@login_required
def history():
    # Query Open jobs under the current user to edit in the future
    posts = Post.query.filter(Post.user_id == current_user.id, Post.status == "Open")
    # Import class Results from tables.py and pass along an iterable object
    table = OpenJobs(posts, no_items="All jobs are submitted. If there any changes required on any previous submission, please contact Production Control IMMEDIATELY.", border='True')
    # Initialize Job header information form
    form = JobDetailsForm()
    # Submit form
    if form.validate_on_submit():
        # Store all form data in a variable
        post = Post(job_start_time=datetime.utcnow(), real_time_scans= form.entry_type.data,table=form.table.data, author=current_user, operation=form.operation.data, pn=form.pn.data, job=form.job.data, rework=form.rework.data, nit=form.nit.data, status="Open")
        # add data to the sqlalchemy object
        db.session.add(post)
        # commit changes to the object to the database
        db.session.commit()
        # message user that production has started.
        flash('Production Started on Job {}{}'.format(form.job.data, " "))
        # redirect to the URL
        if post.real_time_scans == 1 or post.real_time_scans is True:
            return redirect(url_for('complete_sort_box_scan'))
        return redirect(url_for('complete_sort'))
    # render open jobs and the production form
    return render_template('history.html', title='Start production', form=form, table=table)


@app.route('/sorting production', methods=['get', 'post'])
def complete_sort():
    # Get latest entry from database for current user
    users_post = Post.query.filter(Post.user_id == current_user.id).order_by(Post.timestamp.desc()).first()
    # assing id of users transaction id to variable
    users_post_id = users_post.id
    # assign query values to form.
    form = JobProductionForm(rework=users_post.rework, nit=users_post.nit, table=users_post.table, job=users_post.job, pn=users_post.pn, operation=users_post.operation)

    # Update database
    if form.validate_on_submit():
        # Update values
        data_update = {
        'status': 'complete',
        'timestamp': datetime.utcnow(),
        'table': form.table.data,
        'pn': form.pn.data,
        'job': form.job.data,
        'operation': form.operation.data,
        'rework': form.rework.data,
        'nit': form.nit.data,
        'total_pcs': form.labor_quantity.data,
        'good_pcs': form.labor_quantity.data,
        'scrap_pcs': 0,
        'user_modified_after_submission': False,
        'real_time_scans': False,

        # This can be replaced by timestamp? Purpose to record every submission click. Vs. recording every box scan.
        # 'last_submit_time': ,
        # 'job_start_time': #  Not needed

        'job_end_time': datetime.utcnow(), 
        # 'lunch_taken': 
        # 'lunch_start_time': 
        # 'lunch_end_time': 
        # 'break_taken': 
        # 'break_start_time': 
        # 'break_end_time': 
        'notes': form.notes.data,
        'Scrap_blisters': form.scrap_blisters.data,
        'Scrap_plating': form.scrap_plating.data,
        'Scrap_flash': form.scrap_flash.data,
        'Scrap_assembly_issues': form.scrap_assembly_issues.data,
        'Scrap_auto_sort': form.scrap_auto_sort.data,
        'Scrap_bad_threads': form.scrap_bad_threads.data,
        'Scrap_bent': form.scrap_bent.data,
        'Scrap_broken_or_damaged_core': form.scrap_broken_or_damaged_core.data,
        'Scrap_buffing': form.scrap_buffing.data,
        'Scrap_contamination': form.scrap_contamination.data,
        'Scrap_damaged_die': form.scrap_damaged_die.data,
        'Scrap_debris_stuck_in_part': form.scrap_debris_stuck_in_part.data,
        'Scrap_dimensional': form.scrap_dimensional.data,
        'Scrap_gate_vestige': form.scrap_gate_vestige.data,
        'Scrap_heat_sinks': form.scrap_heat_sinks.data,
        'Scrap_high_or_low_ejectors': form.scrap_high_or_low_ejectors.data,
        'Scrap_lamination': form.scrap_lamination.data,
        'Scrap_leak_test_failed': form.scrap_leak_test_failed.data,
        'Scrap_mixed_parts': form.scrap_mixed_parts.data,
        'Scrap_other': form.scrap_other.data,
        'Scrap_part_damage': form.scrap_part_damage.data,
        'Scrap_parts_not_tapped': form.scrap_parts_not_tapped.data,
        'Scrap_parts_on_gates': form.scrap_parts_on_gates.data,
        'Scrap_poor_fill': form.scrap_poor_fill.data,
        'Scrap_porosity': form.scrap_porosity.data,
        'Scrap_skiving': form.scrap_skiving.data,
        'Scrap_soldering_and_dragging': form.scrap_soldering_and_dragging.data,
        'Scrap_start_up_scrap': form.scrap_start_up_scrap.data,
        'Scrap_surface_finish': form.scrap_surface_finish.data,
        'Scrap_trim_damage': form.scrap_trim_damage.data,
        'Scrap_weight_out_of_specification': form.scrap_weight_out_of_specification.data,
        'Scrap_wrong_part': form.scrap_wrong_part.data,

        }
        # Update record id with data from data_update dictionary
        db.session.query(Post).filter_by(id=users_post_id).update(data_update)
        db.session.commit()
        # Message user of sucessful entry.
        flash('Production successfully submitted!! Please remember to log off at the end of your shift. Or start the next production job.')
        return redirect(url_for('history'))
    return render_template('sorting_production.html', title="Production", form=form)


## Testing link column
@app.route('/item/<int:id>', methods=['Get', 'Post'])
def edit(id):
    # query to get the record that matches the Post ID
    qry = Post.query.filter(Post.id == id)
    # assigning that one record and turning it to a non iterable item, im pretty sure.
    transaction = qry.first()
    # assign values of query above to form
    form = JobProductionForm(job=transaction.job, table=transaction.table, pn=transaction.pn, operation=transaction.operation, nit=transaction.nit, rework=transaction.rework)
   
    # Form submitted and passed checks
    if form.validate_on_submit():
        # Update values
        data_update = {
        'status': 'Updated',
        'timestamp': datetime.utcnow(),
        'table': form.table.data,
        'pn': form.pn.data,
        'job': form.job.data,
        'operation': form.operation.data,
        'rework': form.rework.data,
        'nit': form.nit.data,
        'total_pcs': form.labor_quantity.data,
        'good_pcs': form.labor_quantity.data,
        'scrap_pcs': 0,
        'user_modified_after_submission': True,
        # 'real_time_scans': False, #  Not used here as it is an edit page

        # This can be replaced by timestamp? Purpose to record every submission click. Vs. recording every box scan.
        # 'last_submit_time': ,
        # 'job_start_time': #  Not needed

        'job_end_time': datetime.utcnow(), 
        # 'lunch_taken': 
        # 'lunch_start_time': 
        # 'lunch_end_time': 
        # 'break_taken': 
        # 'break_start_time': 
        # 'break_end_time': 
        'notes': form.notes.data,
        'Scrap_blisters': form.scrap_blisters.data,
        'Scrap_plating': form.scrap_plating.data,
        'Scrap_flash': form.scrap_flash.data,
        'Scrap_assembly_issues': form.scrap_assembly_issues.data,
        'Scrap_auto_sort': form.scrap_auto_sort.data,
        'Scrap_bad_threads': form.scrap_bad_threads.data,
        'Scrap_bent': form.scrap_bent.data,
        'Scrap_broken_or_damaged_core': form.scrap_broken_or_damaged_core.data,
        'Scrap_buffing': form.scrap_buffing.data,
        'Scrap_contamination': form.scrap_contamination.data,
        'Scrap_damaged_die': form.scrap_damaged_die.data,
        'Scrap_debris_stuck_in_part': form.scrap_debris_stuck_in_part.data,
        'Scrap_dimensional': form.scrap_dimensional.data,
        'Scrap_gate_vestige': form.scrap_gate_vestige.data,
        'Scrap_heat_sinks': form.scrap_heat_sinks.data,
        'Scrap_high_or_low_ejectors': form.scrap_high_or_low_ejectors.data,
        'Scrap_lamination': form.scrap_lamination.data,
        'Scrap_leak_test_failed': form.scrap_leak_test_failed.data,
        'Scrap_mixed_parts': form.scrap_mixed_parts.data,
        'Scrap_other': form.scrap_other.data,
        'Scrap_part_damage': form.scrap_part_damage.data,
        'Scrap_parts_not_tapped': form.scrap_parts_not_tapped.data,
        'Scrap_parts_on_gates': form.scrap_parts_on_gates.data,
        'Scrap_poor_fill': form.scrap_poor_fill.data,
        'Scrap_porosity': form.scrap_porosity.data,
        'Scrap_skiving': form.scrap_skiving.data,
        'Scrap_soldering_and_dragging': form.scrap_soldering_and_dragging.data,
        'Scrap_start_up_scrap': form.scrap_start_up_scrap.data,
        'Scrap_surface_finish': form.scrap_surface_finish.data,
        'Scrap_trim_damage': form.scrap_trim_damage.data,
        'Scrap_weight_out_of_specification': form.scrap_weight_out_of_specification.data,
        'Scrap_wrong_part': form.scrap_wrong_part.data,
            
        }
        db.session.query(Post).filter_by(id=transaction.id).update(data_update)
        db.session.commit()
        flash("Job {} completed successfully.".format(form.job.data))
        return redirect(url_for('history'))

    flash("Please make the necessary edits to the job started on {}. When complete hit Submit.".format(transaction.timestamp))
    return render_template('edit_production.html', form=form, creation_time=transaction.timestamp)    


@app.route('/sorting production boxscan', methods=['get','post'])
@login_required
def complete_sort_box_scan():
    # Get latest entry from database for current user
    users_post = Post.query.filter(Post.user_id == current_user.id).order_by(Post.timestamp.desc()).first()
    # assing id of users transaction id to variable
    users_post_id = users_post.id
    # assign query total pc quantity to the
    form = BoxScanForm()
    # Form submission update database
    if form.validate_on_submit():
        data_update= {
            # Add to the qty in the db with the qty from the form.
            'good_pcs': users_post.good_pcs + int(form.box_quantity.data),

        }
         # Update record id with data from data_update dictionary
        db.session.query(Post).filter_by(id=users_post_id).update(data_update)
        db.session.commit()
        # Message user of sucessful entry.
        flash('Scan accepted! Your production quantity has been increased. Current  job quantity is {}'.format('adsfd'))
        return redirect(url_for('complete_sort_box_scan'))
    return render_template('sorting_production_boxscan.html', title="Production rt scanning", form=form)



@app.route('/activejobs')
def search_open():
    # query current users open jobs
    posts = Post.query.filter(Post.status == "Open",)
    # Import class Results from tables.py and pass along an iterable object
    table = Results(posts, no_items="There are currently no employees signed into any jobs.", border='True')
    # simple render of all data in a table
    return render_template('results.html', table=table)


@app.route('/completejobs')
def search_complete():
    # query current users open jobs
    posts = Post.query.filter(Post.status == "complete",)
    # Import class Results from tables.py and pass along an iterable object
    table = Results(posts, no_items="There are no records that match this criteria.", border='True')
    # simple render of all data in a table
    return render_template('results.html', table_completes=table)
