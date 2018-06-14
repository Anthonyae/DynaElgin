# routes different URL's that the application uses
# python functions are called view functions and are handlers for the application routes

from app import app, db  # importing db to call sql alchemy to query database
from app.forms import LoginForm, RegistrationForm, JobDetailsForm, JobProductionForm, BoxScanForm, BoxScanValueForm, StaticForm
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
# testing to use func expression - OK TO DELETE. NOT USED
from sqlalchemy.sql.expression import func
# import from tables.py the class that contains views for viewing data in a table
from app.tables import Results, OpenJobs
# import datetime modules
import datetime
from datetime import datetime as d
# import my function for elapsed time
from app.my_functions import elapsed_time, String_time,query_to_list, obj_to_list, to_dict, s_to_string_time
# import regular expressions
import re
import csv
import os

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
        return redirect(url_for('history'))
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
            return redirect(url_for('index'))
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
    # filter_by allows for (keyword = x) i.e  where as filter you can be more pythonic and do (User.name == 'anthony')
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'Notes': 'Under Construction'}
    ]
    return render_template('user.html', user=user, posts=posts)


@app.route('/Production and Open jobs', methods=['Get', 'Post'])
@login_required
def history():
    # Query Open jobs under the current user to edit in the future
    posts = Post.query.filter(Post.user_id == current_user.id, Post.status == "OPEN")
    # Import class Results from tables.py and pass along an iterable object
    table = OpenJobs(posts, no_items="All jobs are submitted. If there any changes required on any previous submission, please contact Production Control or your supervisor!", border='True')
    # Initialize Job header information form
    form = JobDetailsForm()
    # Submit form
    if form.validate_on_submit():
        # Query database for instance of Open job status on the same job number for the current user
        query_job = Post.query.filter(Post.user_id == current_user.id, Post.job == form.job.data, Post.status == "OPEN").first()
        # if query_job is not None then we already have a transaction with that job number that is open.
        if query_job is not None:
            flash('You already have this job {} started! Please review your open jobs and complete it before continuing.'.format(form.job.data))
            return redirect(url_for('history'))

        # Data to be updated. Mix of implicit job information and form information.
        # Store all form data in a variable
        post = Post(job_start_time=datetime.datetime.now(), real_time_scans=form.entry_type.data, table=form.table.data, author=current_user, operation=form.operation.data, pn=form.pn.data, job=form.job.data, rework=form.rework.data, nit=form.nit.data, status="OPEN", timestamp=datetime.datetime.now())
        # add data to the sqlalchemy object
        db.session.add(post)
        # commit changes to the object to the database
        db.session.commit()
        # get id of added transaction
        new_record = Post.query.filter(Post.user_id == current_user.id, Post.status == "OPEN").order_by(Post.id.desc()).first()
        # message user that production has started # d.strftime('ignore',"%b %d %Y %I:%M:%S %p")
        flash('Production Started on Job {} at {}'.format(form.job.data, d.strftime(post.job_start_time , "%b %d %Y %I:%M:%S %p")))
        # redirect to the URL
        if post.real_time_scans == 1 or post.real_time_scans is True:
            return redirect(url_for('complete_sort_box_scan', record=int(new_record.id)))
        return redirect(url_for('complete_sort', record=str(new_record.id)))
    # render open jobs and the production form
    return render_template('history.html', title='Start production', form=form, table=table)


@app.route('/sorting production/<int:record>', methods=['get', 'post'])
def complete_sort(record):
    # Get latest entry from database for current user. first() returns the first obejct in a query. We know it will only be one object.
    users_post = Post.query.filter(Post.id == record).first()
    # assign query values to form.
    form = JobProductionForm(rework=users_post.rework, nit=users_post.nit, table=users_post.table, job=users_post.job, pn=users_post.pn, operation=users_post.operation)
    # Update database
    if form.validate_on_submit():
        # transaction time
        now = datetime.datetime.now()
        # Update values; upon submission of form
        data_update = {
        'status': 'COMPLETE',
        'timestamp': now,
        'table': form.table.data,
        'pn': form.pn.data,
        'job': form.job.data,
        'operation': form.operation.data,
        'rework': form.rework.data,
        'nit': form.nit.data,
        # COMPLETE TOTAL PIECES
        # 'total_pcs': form.labor_quantity.data,
        'good_pcs': form.labor_quantity.data,
        # COMPLETE SCRAP PIECES
        # 'scrap_pcs': 0,
        'user_modified_after_submission': False,
        # Job time details
        # 'real_time_scans': , #  Not applicable here
        # 'last_submit_time': , #  Not applicable here
        # 'job_start_time': , #  Not applicable here
        'job_end_time': datetime.datetime.now(),
        # Job time details expanded - rates
        'job_elapsed_time': elapsed_time(users_post.job_start_time, now),
        # 'job_rate' =  , #  Not applicable here
        # 'job_number_of_scans' = , #  Not applicable here
        # Start of employee pattern information
        # 'lunch_break_taken' = # TO DO HERE
        # 'lunch_break_start_time' = #  TO DO HERE
        # 'lunch_break_end_time' = #  TO DO HERE
        # 'lunch_break_counter' = #  TO DO HERE
        # 'lunch_break_total_time' =  TO DO HERE
        #  Regular columns for scrap and notes
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
        db.session.query(Post).filter_by(id=users_post.id).update(data_update)
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
    # Check if box scan form was used
    if transaction.real_time_scans == 1 or transaction.real_time_scans is True:
        flash("Please make the necessary edits to the job started on {}. When complete hit Submit.".format(d.strftime(transaction.job_start_time,"%b %d %Y %I:%M %p")))
        return redirect(url_for('complete_sort_box_scan',record=id,))
    # assign values of query above to form
    form = JobProductionForm(job=transaction.job, table=transaction.table, pn=transaction.pn, operation=transaction.operation, nit=transaction.nit, rework=transaction.rework)
   
    # Form submitted and passed checks
    if form.validate_on_submit():
        # Current time
        now = datetime.datetime.now()

        # Update values
        data_update = {
        'status': 'UPDATED',
        'timestamp': now,
        'table': form.table.data,
        'pn': form.pn.data,
        'job': form.job.data,
        'operation': form.operation.data,
        'rework': form.rework.data,
        'nit': form.nit.data,
        # COMPLETE TOTAL PIECES
        # 'total_pcs': form.labor_quantity.data,
        'good_pcs': form.labor_quantity.data,
        # COMPLETE SCRAP PIECES
        # 'scrap_pcs': 0,
        'user_modified_after_submission': True,
        # Job time details
        # 'real_time_scans': , #  Not applicable here
        # 'last_submit_time': , #  Not applicable here
        # 'job_start_time': , #  Not applicable here
        'job_end_time': datetime.datetime.now(),
        # Job time details expanded - rates
        'job_elapsed_time': elapsed_time(transaction.job_start_time, now),
        # 'job_rate' =  , #  Not applicable here
        # 'job_number_of_scans' = , #  Not applicable here
        # Start of employee pattern information
        # 'lunch_break_taken' = # TO DO HERE
        # 'lunch_break_start_time' = #  TO DO HERE
        # 'lunch_break_end_time' = #  TO DO HERE
        # 'lunch_break_counter' = #  TO DO HERE
        # 'lunch_break_total_time' =  TO DO HERE
        #  Regular columns for scrap and notes
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

    flash("Please make the necessary edits to the job started on {}. When complete hit Submit.".format(d.strftime(transaction.job_start_time,"%b %d %Y %I:%M %p")))
    return render_template('edit_production.html', form=form, creation_time=transaction.timestamp)    

@login_required
@app.route('/sorting production boxscan/<int:record>', methods=['get','post'])
def complete_sort_box_scan(record):
    # Get latest entry from database for current user
    users_post = Post.query.filter(Post.id == record).first()
    # Form assignment
    form = BoxScanForm()
    # Form submission update database
    if form.validate_on_submit():
        print("valid submit")
        # Retrieve first match of integers being scanned to get box quantity
        box_quantity = int(re.findall('\d+',form.box_quantity.data)[0])
        # Data to be updated in the box scan form.
        # Calculate elapsed job time
        now = datetime.datetime.now()
        dt = users_post.job_start_time
        dt2 = now
        delta = dt2-dt
        s = delta.seconds
        # get amount of pcs
        labor_qty = users_post.good_pcs + box_quantity
        # calculate rate
        rate = round(labor_qty/s*3600,0)
        # Store variables for update
        data_update= {
            # Add to the qty in the db with the qty from the form.
            'good_pcs': labor_qty,
            'last_submit_time': dt2,
            'job_rate': rate,
            'job_number_of_scans': users_post.job_number_of_scans + 1,
        }
         # Update record id with data from data_update dictionary
        db.session.query(Post).filter_by(id=users_post.id).update(data_update)
        db.session.commit()
        # Message user of sucessful entry.
        flash('Scan accepted! Your production quantity has been increased by {} pcs! Current job quantity is {} pcs!'.format(box_quantity, users_post.good_pcs))
        return redirect(url_for('complete_sort_box_scan', record=record, total=users_post.good_pcs))
    return render_template('sorting_production_boxscan.html', title="Production R-T scanning", form=form, variable_id=str(record), total=users_post.good_pcs)


@login_required
@app.route('/sorting production boxscan_negative/<int:record>', methods=['get','post'])
def complete_sort_box_scan_negative(record):
    # Get latest entry from database for current user
    users_post = Post.query.filter(Post.id == record).first()
    # Form assignment
    form = BoxScanForm()
    # Form submission update database
    if form.validate_on_submit():
        # Retrieve first match of integers being scanned to get box quantity
        box_quantity = int(re.findall('\d+',form.box_quantity.data)[0])
        # Error handling of negative transaciton
        negative_check = users_post.good_pcs - box_quantity
        if negative_check < 0:
            flash('This transaction of {} pcs will result in a negative quantity of {} pcs! Please review your selection.'.format(box_quantity, negative_check))
            return redirect(url_for('complete_sort_box_scan_negative', record = record, total = users_post.good_pcs,))

        # Data to be updated in the box scan form.
        # Calculate elapsed job time
        now = datetime.datetime.now()
        dt = users_post.job_start_time
        dt2 = now
        delta = dt2-dt
        s = delta.seconds
        # get amount of pcs
        labor_qty = users_post.good_pcs - box_quantity
        # calculate rate
        rate = round(labor_qty/s*3600,0)
        # Dict of values to update
        data_update= {
            # Add to the qty in the db with the qty from the form.
            'good_pcs': labor_qty,
            'last_submit_time': dt2,
            'job_rate': rate,
            # 'job_number_of_scans': users_post.job_number_of_scans + 1, #  Do not add to scan count as it is not an addition of pcs.
        }
         # Update record id with data from data_update dictionary
        db.session.query(Post).filter_by(id=users_post.id).update(data_update)
        db.session.commit()
        # Message user of sucessful entry.
        flash('Scan accepted! Your production quantity has been decreased by {} pcs! Current job quantity is {} pcs!'.format(box_quantity, users_post.good_pcs))
        return redirect(url_for('complete_sort_box_scan', record=record,))
    return render_template('sorting_production_boxscan_neg.html', title="Production R-T scanning, remove good pcs", form=form, variable_id=str(record),total=users_post.good_pcs,)


@login_required
@app.route('/sorting production boxscan submission/<int:record>', methods=['get', 'post'])
def complete_sort_box_scan_submission(record):
    # Get record passed in from box scan form
    users_post = Post.query.filter(Post.id == int(record))
    # This is the actual single post.
    users_post_single_item = users_post.first()
    # Show user current job details
    table = Results(users_post, no_items="This is an error. Please contact Production Control or turn in a written form.", border='True')
    # Render form to complete update
    form = StaticForm()
    # Form submitted and passed checks
    if form.validate_on_submit():
    # Data to be updated in the static form.
        # Calculate elapsed job time
        now = datetime.datetime.now()
        # Update record
        data_update = {
            'status': 'COMPLETE',
            'timestamp': now,
            # NEED TO COMPLETE = GET ALL SCRAP AND UPDATE TOTAL VALUE
            'job_end_time': now,
            'job_elapsed_time': elapsed_time(users_post_single_item.job_start_time, now), 
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
        db.session.query(Post).filter_by(id=record).update(data_update)
        db.session.commit()
        # Message user of sucessful entry.
        flash('Production successfully submitted!! Please remember to log off at the end of your shift. Or start the next production job.')
        return redirect(url_for('history'))
    return render_template('sorting_production_boxscan_submission.html', table=table, form=form)


@app.route('/break_timer/<int:record>', methods=['get', 'post'])
@login_required
def start_break(record):
    # Get record passed in from box scan form
    users_post = Post.query.filter(Post.id == int(record)).first()
    # Current time
    now = datetime.datetime.now()
    # update data
    data_update = {
        'lunch_break_taken': True,
        'lunch_break_start_time': now,
        'lunch_break_end_time': None ,
        'lunch_break_counter': users_post.lunch_break_counter + 1,
        # 'lunch_break_total_time': ,
    }
    db.session.query(Post).filter_by(id=users_post.id).update(data_update)
    db.session.commit()
    # Message user of successful entry.
    flash('Lunch/break has started on job {}'.format(users_post.job))
    return render_template('lunch_break.html', record=record)
    # return redirect(url_for('end_break', record=record,))

    
@app.route('/break_timer2/<int:record>', methods=['get', 'post'])
@login_required
def end_break(record):
    # Get record passed in from box scan form
    users_post = Post.query.filter(Post.id == int(record)).first()
    # Current time
    now = datetime.datetime.now()
    # previous elapsed time of lunch break total time
    previous_time = users_post.lunch_break_total_time
    print(previous_time)
    # add previous elapsed time(string) to current time duration(timedelta)
    total_time = None
    if previous_time:
        # init class - splits time into a list of [hours,minutes,seconds]
        s_time_object = String_time(previous_time)
        print(s_time_object, "s_time_object, list")
        # change interval list from above into seconds
        s = int(round(s_time_object.string_seconds()))
        print(s,"s, this should be an INT and seconds")
        # convert seconds into a timedelta object NOT NEEDED NOW...
        # delta = datetime.timedelta(seconds=s)

        # init class - this time for the difference between break start time and now
        x = now - users_post.lunch_break_start_time
        print(x, "x, This should be a positive number, type - interval")
        now_s = int(round(datetime.timedelta.total_seconds(x),0))
        print(now_s, "now_s, this should be a positive number and rounded to an integer ")
        # not needed now
        # now_delta = datetime.timedelta(seconds=now_s)

        # add previous timedelta object with current timedelta object
        total_seconds = s + now_s
        print(total_seconds, "total_seconds")
        total_time = s_to_string_time(total_seconds)
        print(total_time, "total_time")
    else:
        total_time = elapsed_time(users_post.lunch_break_start_time,now)
     # update data
    data_update = {
        'lunch_break_taken': False,
        # 'lunch_break_start_time': ,
        'lunch_break_end_time': now ,
        # 'lunch_break_counter': ,
        'lunch_break_total_time': total_time,
    }
    db.session.query(Post).filter_by(id=users_post.id).update(data_update)
    db.session.commit()
    # Message user of successful entry.
    flash('Lunch/break has ended. Please select your job {} to continue production.'.format(users_post.job))
    return redirect(url_for('history', record=record,))

@app.route('/activejobs')
def search_open():
    # query current users open jobs
    posts = Post.query.filter(Post.status == "OPEN",)
    # change the value of attributes for representation to reader
    for record in posts:        
        # setattr(record, 'job_start_time', d.strftime(record.job_start_time,"%b %d %Y %I:%M:%S %p"))
        x = 1
    # Import class Results from tables.py and pass along an iterable object
    table = Results(posts, no_items="There are currently no employees signed into any jobs.", border='True')
    # simple render of all data in a table
    return render_template('results.html', table=table)


@app.route('/completejobs')
def search_complete():
    # query current users open jobs
    posts = Post.query.filter((Post.status == "COMPLETE")|( Post.status == "UPDATED")).all()
    # Import class Results from tables.py and pass along an iterable object
    table = Results(posts, no_items="There are no records that match this criteria.", border='True')

    # simple render of all data in a table

    return render_template('results.html', table_completes=table,)
