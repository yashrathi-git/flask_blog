import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from blog.custom_filter import pretty_date

# Create a login manager object
login_manager = LoginManager()

app = Flask(__name__)

######### CONFIGRATIONS ###################
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL')
app.config['MAIL_PASSWORD'] = os.environ.get('PASSWORD')
app.jinja_env.filters['human_date'] = pretty_date
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
#########################################


mail = Mail(app)



db = SQLAlchemy(app)
Migrate(app, db)

# We can now pass in our app to the login manager
login_manager.init_app(app)

# Tell users what view to go to when they need to login.
login_manager.login_view = "user_accounts.login"

### IMPORT BLUEPRINT ###
from blog.user_accounts.views import user_account_blueprint
from blog.posts.views import posts_blueprint
from blog.profile.views import profile_blueprint
from blog.errors.handlers import errors
### Registering Blueprints ###
app.register_blueprint(user_account_blueprint, url_prefix='/auth')
app.register_blueprint(posts_blueprint,url_prefix='/post')
app.register_blueprint(profile_blueprint, url_prefix='/profile')
app.register_blueprint(errors)

