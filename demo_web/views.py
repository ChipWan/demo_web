#!/usr/bin/python
# -*- coding: <encoding name> -*-
# __author__ = chip wan
# Date: 1/12/2019

import hashlib
import random

from flask import render_template, redirect, request, flash, get_flashed_messages

from demo_web import app, db
from demo_web.models import Image, User
from flask_login import login_user, login_required, logout_user, current_user


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
@login_required
def profile(user_id):
    user = User.query.get(user_id)
    if user is None:
        return redirect('/')
    return render_template('profile.html', user=user)


@app.route('/reg_login/')
def reg_login():
    # if current_user().is_authenticated():
    #   return redirect('/')
    msg = ''
    for m in get_flashed_messages(with_categories=False, category_filter=['reg', 'login']):
        msg += m
    return render_template('login.html', msg=msg)


def flash_msg_with(target, msg, category):
    if msg is not None:
        flash(msg, category=category)
    return redirect(target)


@app.route('/reg/', methods={'post'})
def reg():
    # request.args---url里的参数
    # request.form---body里的参数
    user_name = request.values.get('username').strip()
    password = request.values.get('password').strip()
    if user_name is None or password is None:
        return flash_msg_with('/reg_login/', u'用户名或密码不能为空', category='reg')
    user = User.query.filter_by(user_name=user_name).first()
    if user is not None:
        return flash_msg_with('/reg_login/', u'用户名已存在', category='reg')
    # 其他合法性判断
    salt_resource = '1234567890abcdefABCDEF'  # salt 可以改进
    salt = ''.join(random.sample(salt_resource, 8))
    m = hashlib.md5()
    m.update((password + salt).encode("utf8"))
    password = m.hexdigest()
    user = User(user_name, password, salt)
    db.session.add(user)
    db.session.commit()
    login_user(user)
    return redirect('/')


@app.route('/login/', methods={'post'})
def login():
    user_name = request.values.get('username').strip()
    password = request.values.get('password').strip()
    if user_name is None or password is None:
        return flash_msg_with('/reg_login/', u'用户名或密码不能为空', category='login')
    user = User.query.filter_by(user_name=user_name).first()
    if user is None:
        return flash_msg_with('/reg_login/', u'用户不存在', category='login')
    m = hashlib.md5()
    m.update((password + user.salt).encode('utf8'))
    password = m.hexdigest()
    if password != user.password:
        return flash_msg_with('/reg_login/', u'用户名或密码错误', category='login')
    login_user(user)
    return redirect('/')


@app.route('/logout/')
def logout():
    logout_user()
    return redirect('/')
