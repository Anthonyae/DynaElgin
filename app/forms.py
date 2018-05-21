from flask_wtf import FlaskForm  # Base class; used to inherit for our created forms
# For each field, an object is created as a class variable in the LoginForm class. Each field given a description or label as a first argument.
from wtforms import StringField, PasswordField, BooleanField, SubmitField,StringField, RadioField
# Validators used to attach validation behaviors to field.
from wtforms.validators import DataRequired, Optional, EqualTo, Email, ValidationError, Regexp
# IMPORTANT needed to query the database to check if user already exist or not. IN RegistrationForm
from app.models import User
import re


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])  # Form validators generate descriptive error messages on their own already.i.e "Required" for DataRequired()
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class JobDetailsForm(FlaskForm):
    rework = BooleanField('Rework?', validators=[Optional()])
    entry_type = BooleanField('Box-Scan submission?', validators=[Optional()])
    nit = StringField('Nit?', validators=[Regexp(message='Not a likely NIT Number', regex=r'^(\d{5}\d?)$'), Optional()])
    table = StringField('Table #', validators=[DataRequired()])
    job = StringField('Job:', validators=[Regexp(message='Not a possible job number', regex=r'^0[6-7]\d{4}$'), DataRequired()])
    pn = StringField('Part Number:', validators=[Regexp(message='Not a possible part number', regex=r'^(922\d{4})$'), DataRequired()])
    operation = StringField('Operation:', validators=[Regexp(message='Not a possible operation number', regex=r'^[0-9][0-9]$'), DataRequired()])
    submit = SubmitField('Start Production')


class BoxScanForm(FlaskForm):
    # to add radio button, once i know how it works....
    box_quantity = StringField('Please scan box quantity:', validators=[DataRequired()])
    scan_validation = StringField('Please scan the job number', validators=[DataRequired(), Regexp(regex=r'^0[6-7]\d{4}$', message='This is not a possible job number')])
    submit = SubmitField('Scan to submit')


class BoxScanValueForm(FlaskForm):
    production_value = RadioField('Select negative if you are subtracting a box', default='1', choices=[('1', 'Add box quantity'), ('2', 'Remove box quantity')])


class JobProductionForm(FlaskForm):
    # scrap fields for sorting
    rework = BooleanField('Rework?', validators=[Optional()])
    nit = StringField('Nit?', validators=[Regexp(message='Not a likely NIT Number', regex=r'^(\d{5}\d?)$'), Optional()])
    table =StringField('Table #', validators=[DataRequired()])
    job = StringField('Job:', validators=[Regexp(message='Not a possible job number', regex=r'^0[6-7]\d{4}$'), DataRequired()])
    pn = StringField('Part Number:', validators=[Regexp(message='Not a possible part number', regex=r'^(922\d{4})$'), DataRequired()])
    operation = StringField('Operation:', validators=[Regexp(regex=r'^[0-9][0-9]$', message='Not a possible operation number '), DataRequired()])
    scrap_assembly_issues = StringField('Assembly issues:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_auto_sort =StringField('Auto sort:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_bad_threads =StringField('Bad threads:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_bent =StringField('Bent:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_blisters =StringField('Blisters:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_broken_or_damaged_core =StringField('Broken or damaged core:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_buffing =StringField('Buffing:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_contamination =StringField('Contamination:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_damaged_die =StringField('Damaged die:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_debris_stuck_in_part =StringField('Debris stuck in part:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_dimensional =StringField('Dimensional:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_flash =StringField('Flash:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_gate_vestige =StringField('Gate vestigage:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_heat_sinks =StringField('Heat sinks:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_high_or_low_ejectors =StringField('High or low ejectors:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_lamination =StringField('Lamination:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_leak_test_failed =StringField('Leak test failed:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_mixed_parts =StringField('Mixed parts:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_other =StringField('Other:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_part_damage =StringField('Part Damage:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_parts_not_tapped =StringField('Parts not tapped:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_parts_on_gates =StringField('Parts on gates:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_plating =StringField('Plating:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_poor_fill =StringField('Poor fill:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_porosity =StringField('Porosity:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_skiving =StringField('Skiving:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_soldering_and_dragging =StringField('Soldering and dragging:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_start_up_scrap =StringField('Start up scrap:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_surface_finish =StringField('Surface finish:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_trim_damage =StringField('Trim damage:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_weight_out_of_specification =StringField('Weight out of specification:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_wrong_part =StringField('Wrong part:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    # Total bad pcs and possible good pcs
    notes = StringField("Notes/comments:", validators=[Optional()])
    labor_quantity =StringField('Good pieces:', validators=[DataRequired()])
    submit_production = SubmitField('Submit Production')

class StaticForm(FlaskForm):
    # scrap fields for sorting
    scrap_assembly_issues = StringField('Assembly issues:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_auto_sort =StringField('Auto sort:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_bad_threads =StringField('Bad threads:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_bent =StringField('Bent:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_blisters =StringField('Blisters:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_broken_or_damaged_core =StringField('Broken or damaged core:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_buffing =StringField('Buffing:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_contamination =StringField('Contamination:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_damaged_die =StringField('Damaged die:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_debris_stuck_in_part =StringField('Debris stuck in part:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_dimensional =StringField('Dimensional:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_flash =StringField('Flash:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_gate_vestige =StringField('Gate vestigage:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_heat_sinks =StringField('Heat sinks:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_high_or_low_ejectors =StringField('High or low ejectors:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_lamination =StringField('Lamination:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_leak_test_failed =StringField('Leak test failed:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_mixed_parts =StringField('Mixed parts:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_other =StringField('Other:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_part_damage =StringField('Part Damage:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_parts_not_tapped =StringField('Parts not tapped:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_parts_on_gates =StringField('Parts on gates:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_plating =StringField('Plating:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_poor_fill =StringField('Poor fill:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_porosity =StringField('Porosity:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_skiving =StringField('Skiving:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_soldering_and_dragging =StringField('Soldering and dragging:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_start_up_scrap =StringField('Start up scrap:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_surface_finish =StringField('Surface finish:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_trim_damage =StringField('Trim damage:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_weight_out_of_specification =StringField('Weight out of specification:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    scrap_wrong_part =StringField('Wrong part:', validators=[Regexp(regex=r'\b([0-9]|[1-9][0-9]|1[0-9][0-9]|[0-9][0-9][0-9][0-9])\b', message='Not a likely scrap quantity'), Optional()])
    # Total bad pcs and possible good pcs
    notes = StringField("Notes/comments:", validators=[Optional()])
    submit_production = SubmitField('Submit Production')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    # When you add any methods that match the pattern "validate_<field_name>", WTForms takes those as customer validators and invokes them in adddition to the stock validators.
    # Here we are checking that the username and password are not already in the database.

    def validate_username(self, username):
        # filter database to find username
        user = User.query.filter_by(username=username.data).first()
        # if username is found trigger ValidationError by raising one.
        if user is not None:
            raise ValidationError('This username already has an account')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('This email address is already used for another account.')
