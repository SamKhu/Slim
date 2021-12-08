from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///slim4.db'
app.config['SECRET_KEY']='ebdc451ec58fec34cb97f207'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


from slim import routes
