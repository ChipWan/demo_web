#!/usr/bin/python
# -*- coding: <encoding name> -*-
# __author__ = chip wan
# Date: 1/12/2019

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.jinja_env.line_statement_prefix='#'
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.config.from_pyfile('app.conf')
db = SQLAlchemy(app)
from demo_web import views, models
