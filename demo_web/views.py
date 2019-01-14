#!/usr/bin/python
# -*- coding: <encoding name> -*-
# __author__ = chip wan
# Date: 1/12/2019

from demo_web import app
from flask import render_template, redirect
from demo_web.models import Image, User


@app.route('/')
def index():
    images = Image.query.order_by('id desc').limit(10).all()
    return render_template('index.html', images=images)


@app.route('/image/<int:image_id>/')
def image_page(image_id):
    image = Image.query.get(image_id)
    if image is None:
        return redirect('/')
    return render_template('pageDetail.html', image=image)


@app.route('/profile/<int:user_id>/')
def profile(user_id):
    user = User.query.get(user_id)
    if user is None:
        return redirect('/')
    return render_template('profile.html', user=user)
