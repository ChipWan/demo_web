#!/usr/bin/python
# -*- coding: <encoding name> -*-
# __author__ = chip wan
# Date: 1/12/2019

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.jinja_env.line_statement_prefix = '#'
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.config.from_pyfile('app.conf')
app.secret_key = 'unique'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = '/reg_login/'
from demo_web import views, models
