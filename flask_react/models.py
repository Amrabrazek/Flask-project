from flask_react import db, login_manager
from datetime import datetime, date
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User (db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    middle_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    birth_date = db.Column(db.DateTime(), nullable=False)

    # image = db.Column(db.String(255), nullable=True)
    profile_image_data = db.Column(db.LargeBinary, nullable=True)
    profile_image_filename = db.Column(db.String(100), nullable=True)

    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False )
    posts = db.relationship('Post', backref='author', lazy=True)
    # friends = db.relationship('Friendship', backref='author', lazy=False)

    def __repr__(self):
        return f"User:{self.username}, email: {self.email}"

class Friendship(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    friend_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)


class Friendshiprequest(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    friend_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    # status = db.Column(db.String(10), nullable=False,  choices=['accepted', 'refused'])


class Post (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default = datetime.now())
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(10), nullable=False, default='public')
    # status = db.Column(db.String(10), nullable=False, default='public', choices=['public', 'friends', 'onlyme'])
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
