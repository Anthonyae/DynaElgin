import os
# loads a file before config class is created. So that variables are set when the class is created
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env')) # Added to add the .env file to the Mysql loadup

# Configuration class for the application. Settings are defined as class variables inside the Config class
# Configuration items can be added to this class.
class Config(object):
    # Secret key protects site from seasurf. Value of key is  set as an expression with two terms joinged by "or" operator.
    # First term looks for the environment variable "Secret_Key". 
    # Second term is just a hardcoded string. 
    # If not first one then default to second term.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # Flask-SqlAlchemy extention takes the location of the application's database from this configuration varialbes.
    # also proveds fallback value when the environment does not define the variable.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    # feature can signal the application every time a change is about to be made in the databse
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Used to send emails of errors
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['anthony.ae@outlook.com']

    # Option for logging.
    Log_TO_STDOUT= os.environ.get('LOG_TO_-STDOUT')    
