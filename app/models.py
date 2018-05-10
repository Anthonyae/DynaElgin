from app import db, login  # login - function that can be called to load a user given the ID from flask's user session (storage space for each user connected to app)
from datetime import datetime
# imports from core dependency of flask
# create hash of argument given to generate and verify's with check function
from werkzeug.security import generate_password_hash, check_password_hash
# Flask-login requires 4 items to be added to the user model to work. Shortcut is UserMixin class
from flask_login import UserMixin


# User class inherits from db.model, a base class for all models from Flask-SQLAlchemy. Defines fields as variables.
# Fields are instances of the db.Column class, which takes the field type as an argument, plus other optional arguments
    # such as which fields are unique and indexed.
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    temppassword = db.Column(db.String(128))
    # posts class initiated with db.relationship. Not an actual field, but high-level view of the relationship between users and posts. Not in the database diagram.
    # One-to-many relationship - db.relationship definied on the "one" side.
        # First argument - model class that represents the "many" side of the relationship. (string with class name IF model defined late in module.)
        # Backref - defines the name of a field that will be added to the objects of the "many" class that points back the "one" object.
        # lazy - defines how the database query for the relationship will be issued.
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# function - called to load a user given the ID. 
@login.user_loader
def load_user(id):
    # Need to convert to string because the id that flask-login passes to the function as an argument is going to be a string.
    return User.query.get(int(id))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(15), default="open")
    # When you pass a function as a "default='' " SQLAlchemy will set the field to the value of calling that function.
    # Note that we did not include () after utcnow. We are passing the function itself - not the result of calling it. 
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # Possibly add last_seen
    # Foreign key - here we use lower case to reference the table "Users" in our model. We use uppercase and the class in db.relationship() however.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    table = db.Column(db.Integer)
    pn = db.Column(db.Integer)
    job = db.Column(db.Integer)
    operation = db.Column(db.Integer)
    rework = db.Column(db.Boolean, default=False)
    nit = db.Column(db.Integer)
    total_pcs = db.Column(db.Integer,)
    good_pcs = db.Column(db.Integer, default=0)
    scrap_pcs = db.Column(db.Integer, default=0)
    # Start of maybe columns
    user_modified_after_submission = db.Column(db.Boolean, default=False)
    real_time_scans = db.Column(db.Boolean)
    last_submit_time = db.Column(db.DateTime)
    job_start_time = db.Column(db.DateTime)
    job_end_time = db.Column(db.DateTime)
    lunch_taken = db.Column(db.Boolean, default=False)
    lunch_start_time = db.Column(db.DateTime)
    lunch_end_time = db.Column(db.DateTime)
    break_taken = db.Column(db.Boolean, default=False)
    break_start_time = db.Column(db.DateTime)
    break_end_time = db.Column(db.DateTime)
    notes = db.Column(db.String(64))
    # Scrap columns
    Scrap_blisters = db.Column(db.Integer, default=0)
    Scrap_plating = db.Column(db.Integer, default=0)
    # addeded column to test migrate (flash). Then added the rest of the scrap columns
    Scrap_flash = db.Column(db.Integer, default=0)
    Scrap_assembly_issues = db.Column(db.Integer, default=0)
    Scrap_auto_sort = db.Column(db.Integer, default=0)
    Scrap_bad_threads = db.Column(db.Integer, default=0)
    Scrap_bent = db.Column(db.Integer, default=0)
    Scrap_broken_or_damaged_core = db.Column(db.Integer, default=0)
    Scrap_buffing = db.Column(db.Integer, default=0)
    Scrap_contamination = db.Column(db.Integer, default=0)
    Scrap_damaged_die = db.Column(db.Integer, default=0)
    Scrap_debris_stuck_in_part = db.Column(db.Integer, default=0)
    Scrap_dimensional = db.Column(db.Integer, default=0)
    Scrap_gate_vestige = db.Column(db.Integer, default=0)
    Scrap_heat_sinks = db.Column(db.Integer, default=0)
    Scrap_high_or_low_ejectors = db.Column(db.Integer, default=0)
    Scrap_lamination = db.Column(db.Integer, default=0)
    Scrap_leak_test_failed = db.Column(db.Integer, default=0)
    Scrap_mixed_parts = db.Column(db.Integer, default=0)
    Scrap_other = db.Column(db.Integer, default=0)
    Scrap_part_damage = db.Column(db.Integer, default=0)
    Scrap_parts_not_tapped = db.Column(db.Integer, default=0)
    Scrap_parts_on_gates = db.Column(db.Integer, default=0)
    Scrap_poor_fill = db.Column(db.Integer, default=0)
    Scrap_porosity = db.Column(db.Integer, default=0)
    Scrap_skiving = db.Column(db.Integer, default=0)
    Scrap_soldering_and_dragging = db.Column(db.Integer, default=0)
    Scrap_start_up_scrap = db.Column(db.Integer, default=0)
    Scrap_surface_finish = db.Column(db.Integer, default=0)
    Scrap_trim_damage = db.Column(db.Integer, default=0)
    Scrap_weight_out_of_specification = db.Column(db.Integer, default=0)
    Scrap_wrong_part = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Post {},{},{},{},{},{},{}>'.format(self.timestamp, self.user_id, self.pn, self.job, self.total_pcs, self.rework, self.status)


# Four required items for flask-login:

# is_authenticated: a property that is True if the user has valid credentials or False otherwise.
# is_active: a property that is True if the user's account is active or False otherwise.
# is_anonymous: a property that is False for regular users, and True for a special, anonymous user.
# get_id(): a method that returns a unique identifier for the user as a string (unicode, if using Python 2).