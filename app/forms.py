from flask_wtf import FlaskForm  # Base class; used to inherit for our created forms
# For each field, an object is created as a class variable in the LoginForm class. Each field given a description or label as a first argument.
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, RadioField
# Validators used to attach validation behaviors to field.
from wtforms.validators import DataRequired, Optional, EqualTo, Email, ValidationError
# IMPORTANT needed to query the database to check if user already exist or not. IN RegistrationForm
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])  # Form validators generate descriptive error messages on their own already.i.e "Required" for DataRequired()
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class JobDetailsForm(FlaskForm):
    rework = BooleanField('Rework?', validators=[Optional()])
    entry_type = BooleanField('Box-Scan submission?', validators=[Optional()])
    nit = IntegerField('Nit?', validators=[Optional()])
    table = IntegerField('Table #', validators=[DataRequired()])
    job = IntegerField('Job:', validators=[DataRequired()])
    pn = IntegerField('Part Number:', validators=[DataRequired()])
    operation = IntegerField('Operation:', validators=[DataRequired()])
    submit = SubmitField('Start Production')


class BoxScanForm(FlaskForm):
    # to add radio button, once i know how it works....
    box_quantity = StringField('Please scan box quantity:', validators=[DataRequired()])
    submit = SubmitField('Scan to submit')


class JobProductionForm(FlaskForm):
    # scrap fields for sorting
    rework = BooleanField('Rework?', validators=[Optional()])
    nit = IntegerField('Nit?', validators=[Optional()])
    table = IntegerField('Table #', validators=[DataRequired()])
    job = IntegerField('Job:', validators=[DataRequired()])
    pn = IntegerField('Part Number:', validators=[DataRequired()])
    operation = IntegerField('Operation:', validators=[DataRequired()])
    scrap_assembly_issues = StringField('Assembly issues:', validators=[Optional()])
    scrap_auto_sort = IntegerField('Auto sort:', validators=[Optional()])
    scrap_bad_threads = IntegerField('Bad threads:', validators=[Optional()])
    scrap_bent = IntegerField('Bent:', validators=[Optional()])
    scrap_blisters = IntegerField('Blisters:', validators=[Optional()])
    scrap_broken_or_damaged_core = IntegerField('Broken or damaged core:', validators=[Optional()])
    scrap_buffing = IntegerField('Buffing:', validators=[Optional()])
    scrap_contamination = IntegerField('Contamination:', validators=[Optional()])
    scrap_damaged_die = IntegerField('Damaged die:', validators=[Optional()])
    scrap_debris_stuck_in_part = IntegerField('Debris stuck in part:', validators=[Optional()])
    scrap_dimensional = IntegerField('Dimensional:', validators=[Optional()])
    scrap_flash = IntegerField('Flash:', validators=[Optional()])
    scrap_gate_vestige = IntegerField('Gate vestigage:', validators=[Optional()])
    scrap_heat_sinks = IntegerField('Heat sinks:', validators=[Optional()])
    scrap_high_or_low_ejectors = IntegerField('High or low ejectors:', validators=[Optional()])
    scrap_lamination = IntegerField('Lamination:', validators=[Optional()])
    scrap_leak_test_failed = IntegerField('Leak test failed:', validators=[Optional()])
    scrap_mixed_parts = IntegerField('Mixed parts:', validators=[Optional()])
    scrap_other = IntegerField('Other:', validators=[Optional()])
    scrap_part_damage = IntegerField('Part Damage:', validators=[Optional()])
    scrap_parts_not_tapped = IntegerField('Parts not tapped:', validators=[Optional()])
    scrap_parts_on_gates = IntegerField('Parts on gates:', validators=[Optional()])
    scrap_plating = IntegerField('Plating:', validators=[Optional()])
    scrap_poor_fill = IntegerField('Poor fill:', validators=[Optional()])
    scrap_porosity = IntegerField('Porosity:', validators=[Optional()])
    scrap_skiving = IntegerField('Skiving:', validators=[Optional()])
    scrap_soldering_and_dragging = IntegerField('Soldering and dragging:', validators=[Optional()])
    scrap_start_up_scrap = IntegerField('Start up scrap:', validators=[Optional()])
    scrap_surface_finish = IntegerField('Surface finish:', validators=[Optional()])
    scrap_trim_damage = IntegerField('Trim damage:', validators=[Optional()])
    scrap_weight_out_of_specification = IntegerField('Weight out of specification:', validators=[Optional()])
    scrap_wrong_part = IntegerField('Wrong part:', validators=[Optional()])
    # Total bad pcs and possible good pcs
    notes = StringField("Notes/comments:", validators=[Optional()])
    labor_quantity = IntegerField('Good pieces:', validators=[DataRequired()])
    submit_production = SubmitField('Submit Production')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    # When you add any methods that match the patter "validate_<field_name>", WTForms takes those as customer validators and invokes them in adddition to the stock validators.
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
