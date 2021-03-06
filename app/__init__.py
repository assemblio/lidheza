from flask import Flask
import os
import ConfigParser
from logging.handlers import RotatingFileHandler
from flask.ext.pymongo import PyMongo
from app.utils.utils import Utils
from app.utils.mail_utils import  MailUtils
from app.utils.mongo_utils import MongoUtils
from flask.ext.cors import CORS

# Create MongoDB database object.
mongo = PyMongo()

# Initialize generic utils class
utils = Utils()
mail_utils = MailUtils()

# Initialize mongo access point
mongo_utils = MongoUtils(mongo)

def create_app():
    # Here we  create flask instance
    app = Flask(__name__)

    # Load application configurations
    load_config(app)

    # Configure logging.
    configure_logging(app)

    # Init modules
    init_modules(app)

    # Allow cross-domain access .
    cors = CORS(app, resources={r"/[fetch|click]/*": {"origins": "*"}})

    # Initialize the app to work with MongoDB
    mongo.init_app(app, config_prefix='MONGO')

    return app


def load_config(app):
    ''' Reads the config file and loads configuration properties into the Flask app.
    :param app: The Flask app object.
    '''
    # Get the path to the application directory, that's where the config file resides.
    par_dir = os.path.join(__file__, os.pardir)
    par_dir_abs_path = os.path.abspath(par_dir)
    app_dir = os.path.dirname(par_dir_abs_path)

    # Read config file
    config = ConfigParser.RawConfigParser()
    config_filepath = app_dir + '/config.cfg'
    config.read(config_filepath)

    app.config['SERVER_HOST'] = config.get('Application', 'SERVER_HOST')
    app.config['SERVER_PORT'] = config.get('Application', 'SERVER_PORT')
    app.config['MONGO_DBNAME'] = config.get('Mongo', 'DB_NAME')

    # Set the secret key, keep this really secret, we use it to secure wtform filed data
    app.secret_key = config.get('Application', 'SECRET_KEY')

    # Ad asset upload configs
    allowed_extensions = config.get('Application', 'ALLOWED_EXT')
    app.config['ALLOWED_EXTENSIONS'] = set(allowed_extensions.split(','))

    app.config['UPLOAD_FOLDER'] = config.get('Application', 'UPLOAD_FOLDER')
    app.config['AD_ASSET_REL_FOLDER_URL'] = config.get('Application', 'AD_ASSET_REL_FOLDER_URL')

    # Commission
    app.config['COMMISSION'] = config.get('Application', 'COMMISSION')

    # MAILGUN
    app.config['MAIL_GUN_API_KEY'] = config.get('MailGun', 'API_KEY')
    app.config['MAIL_GUN_API_BASE_URL'] = config.get('MailGun', 'API_BASE_URL')

    # Logging path might be relative or starts from the root.
    # If it's relative then be sure to prepend the path with the application's root directory path.
    log_path = config.get('Logging', 'PATH')
    if log_path.startswith('/'):
        app.config['LOG_PATH'] = log_path
    else:
        app.config['LOG_PATH'] = app_dir + '/' + log_path

    app.config['LOG_LEVEL'] = config.get('Logging', 'LEVEL').upper()


def configure_logging(app):
    ''' Configure the app's logging.
     param app: The Flask app object
    '''

    log_path = app.config['LOG_PATH']
    log_level = app.config['LOG_LEVEL']

    # If path directory doesn't exist, create it.
    log_dir = os.path.dirname(log_path)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Create and register the log file handler.
    log_handler = RotatingFileHandler(log_path, maxBytes=250000, backupCount=5)
    log_handler.setLevel(log_level)
    app.logger.addHandler(log_handler)

    # First log informs where we are logging to.
    # Bit silly but serves  as a confirmation that logging works.
    app.logger.info('Logging to: %s', log_path)


def init_modules(app):

    # Import blueprint modules
    from app.mod_entry_point.views import mod_entry_point
    from app.mod_publisher.views import mod_publisher
    from app.mod_advertiser.views import mod_advertiser
    from app.mod_mail.views import mod_mail
    from app.mod_serve.views import mod_serve

    app.register_blueprint(mod_entry_point)
    app.register_blueprint(mod_publisher)
    app.register_blueprint(mod_advertiser)
    app.register_blueprint(mod_mail)
    app.register_blueprint(mod_serve)
