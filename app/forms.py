from flask_wtf import FlaskForm  # Base class; used to inherit for our created forms
# For each field, an object is created as a class variable in the LoginForm class. Each field given a description or label as a first argument.
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
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
    nit = IntegerField('Nit?', validators=[Optional()])
    table = IntegerField('Table #', validators=[DataRequired()])
    job = IntegerField('Job:', validators=[DataRequired()])
    pn = IntegerField('Part Number:', validators=[DataRequired()])
    operation = IntegerField('Operation:', validators=[DataRequired()])
    submit = SubmitField("Start Production")


class JobProductionForm(FlaskForm):
    # scrap fields for sorting
    rework = BooleanField('Rework?', validators=[Optional()])
    nit = IntegerField('Nit?', validators=[Optional()])
    table = IntegerField('Table #', validators=[DataRequired()])
    job = IntegerField('Job:', validators=[DataRequired()])
    pn = IntegerField('Part Number:', validators=[DataRequired()])
    operation = IntegerField('Operation:', validators=[DataRequired()])
    scrap_assembly_issues = StringField('assembly issues', validators=[Optional()])
    scrap_auto_sort = IntegerField('auto_sort', validators=[Optional()])
    scrap_bad_threads = IntegerField('bad_threads', validators=[Optional()])
    scrap_bent = IntegerField('bent', validators=[Optional()])
    scrap_blisters = IntegerField('blisters', validators=[Optional()])
    scrap_broken_or_damaged_core = IntegerField('broken_or_damaged_core', validators=[Optional()])
    scrap_buffing = IntegerField('buffing', validators=[Optional()])
    scrap_contamination = IntegerField('contamination', validators=[Optional()])
    scrap_damaged_die = IntegerField('damaged_die', validators=[Optional()])
    scrap_debris_stuck_in_part = IntegerField('debris_stuck_in_part', validators=[Optional()])
    scrap_dimensional = IntegerField('dimensional', validators=[Optional()])
    scrap_flash = IntegerField('flash', validators=[Optional()])
    scrap_gate_vestige = IntegerField('gate_vestige', validators=[Optional()])
    scrap_heat_sinks = IntegerField('heat_sinks', validators=[Optional()])
    scrap_high_or_low_ejectors = IntegerField('high_or_low_ejectors', validators=[Optional()])
    scrap_lamination = IntegerField('lamination', validators=[Optional()])
    scrap_leak_test_failed = IntegerField('leak_test_failed', validators=[Optional()])
    scrap_mixed_parts = IntegerField('mixed_parts', validators=[Optional()])
    scrap_other = IntegerField('other', validators=[Optional()])
    scrap_part_damage = IntegerField('part_damage', validators=[Optional()])
    scrap_parts_not_tapped = IntegerField('parts_not_tapped', validators=[Optional()])
    scrap_parts_on_gates = IntegerField('parts_on_gates', validators=[Optional()])
    scrap_plating = IntegerField('plating', validators=[Optional()])
    scrap_poor_fill = IntegerField('poor_fill', validators=[Optional()])
    scrap_porosity = IntegerField('porosity', validators=[Optional()])
    scrap_skiving = IntegerField('skiving', validators=[Optional()])
    scrap_soldering_and_dragging = IntegerField('soldering_and_dragging', validators=[Optional()])
    scrap_start_up_scrap = IntegerField('start_up_scrap', validators=[Optional()])
    scrap_surface_finish = IntegerField('surface_finish', validators=[Optional()])
    scrap_trim_damage = IntegerField('trim_damage', validators=[Optional()])
    scrap_weight_out_of_specification = IntegerField('weight_out_of_specification', validators=[Optional()])
    scrap_wrong_part = IntegerField('wrong_part', validators=[Optional()])
    # Total bad pcs and possible good pcs
    notes = StringField("Notes/comments", validators=[Optional()])
    labor_quantity = IntegerField('Good Pcs', validators=[DataRequired()])
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
