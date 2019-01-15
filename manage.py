#!/usr/bin/python
# -*- coding: <encoding name> -*-
# __author__ = chip wan
# Date: 1/12/2019

from demo_web import app, db
from flask_script import Manager
from demo_web.models import User, Image, Comment
import random
from sqlalchemy import or_, and_

manager = Manager(app)


def get_image_url():
    return '/static/images/' + str(random.randint(0, 10)) + 'm.jpg'


@manager.command
def init_database():
    db.drop_all()
    db.create_all()
    for i in range(100):
        db.session.add(User('user' + str(i + 1), 'a' + str(i)))
        for j in range(3):
            db.session.add(Image(get_image_url(), i + 1))
            for k in range(3):
                db.session.add(Comment('this is ' + str(k) + 'th comment.', i * 3 + j + 1, i + 1))
    db.session.commit()

    for i in range(50, 100, 2):
        user = User.query.get(i)
        user.user_name = '[even]' + user.user_name
    User.query.filter_by(id=1).update({'user_name': '[just_No_1]'})
    # db.session.delete(Comment.query.get(2))
    db.session.commit()

    print(User.query.all())
    print(User.query.get(3))
    print(User.query.filter_by(id=5).first())
    print(User.query.order_by(User.id.desc()).offset(5).limit(3).all())
    print(User.query.filter(User.user_name.endswith('0')).limit(3).all())
    print(User.query.filter(or_(and_(User.id >= 50, User.id <= 52), User.id > 99)).all())
    # print(User.query.filter(id == 101).first_or_404())
    print(User.query.order_by(User.id.desc()).paginate(page=1, per_page=10).items)
    user = User.query.get(1)
    print(user)
    print(user.images)
    image = Image.query.get(1)
    print(image.user)


if __name__ == '__main__':
    manager.run()
