from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# flask-login manages the user logged-in state. Allows application to "remeber" a user moving between pages of website. 
    # 1) add the four required items to User model. Inherit "UserMixing" to the User class
    # 2) Create route @loging.user_loader in models.py - called to load a user given the ID. Used to help flask load a user.
        # Application now has access to the user database.
# extension to incorporate "Moment.js" - javascript library that renders date and time easily
from flask_moment import Moment
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
# Python package writes logs and can email
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler


# # Send email of errors
# if not app.debug:
#     if app.config['MAIL_SERVER']:
#         auth = None
#         if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
#             auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
#         secure = None
#         if app.config['MAIL_USE_TLS']:
#             secure = ()
#         mail_handler = SMTPHandler(
#             mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
#             fromaddr='no-reply@' + app.config['MAIL_SERVER'],
#             toaddrs=app.config['ADMINS'], subject='Microblog Failure',
#             credentials=auth, secure=secure)
#         mail_handler.setLevel(logging.ERROR)
#         app.logger.addHandler(mail_handler)

# Save errors to 10kb file
# if not app.debug:
#     # ...

#     if not os.path.exists('logs'):
#         os.mkdir('logs')
#     file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
#                                        backupCount=10)
#     file_handler.setFormatter(logging.Formatter(
#         '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
#     file_handler.setLevel(logging.INFO)
#     app.logger.addHandler(file_handler)

#     app.logger.setLevel(logging.INFO)
#     app.logger.info('Dynacast startup')


# the __name__ variable is predefined. is set to the name of the module in which it is used.
# flask uses the location of the module passed here as a starting point to load resources, templates
app = Flask(__name__)
# Tells Flask to read config file and apply it
app.config.from_object(Config)
# Database represented by this database instace.
db = SQLAlchemy(app)
# Database migration engine will also have an instance.
migrate = Migrate(app, db)
# Flask-login created and initialized right after application instance
login = LoginManager(app)
# allows - force users to login by redirecting them back to the login form, and only redirect back to the page the user wanted to view after the login process is complete
# To work Flask-login needs to know what is the view function that handles logings.
login.login_view = 'login'
# Init flask-bootstrap extension like other flask extensions
bootstrap = Bootstrap(app)
# extension for rendering javascript code in the client.
moment = Moment(app)


# models - defines the structure of the database
from app import routes, models, errors
