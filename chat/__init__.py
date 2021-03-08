from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.static_folder = 'static'
app.config['SECRET_KEY'] = '0ca5e3a1c2dc3391f9a2bb9c54a532a3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'admin_login'

from chat import routes
