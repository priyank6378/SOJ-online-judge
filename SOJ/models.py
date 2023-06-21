from datetime import datetime
from itsdangerous import URLSafeSerializer as Serializer
from flask import current_app
from SOJ import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    prob_id = db.Column(db.Integer, nullable=False)
    code = db.Column(db.String(10000), nullable=False)
    language = db.Column(db.String(10), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    runtime = db.Column(db.String(10), nullable=False, default="0")
    status = db.Column(db.String(1), nullable=False, default="U") # U->unsolved A->accepted W->wrong


class Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    statement = db.Column(db.String(1000), nullable=False)
    categories = db.Column(db.String(1000), nullable=True)
    input = db.Column(db.String(1000), nullable=False)
    output = db.Column(db.String(1000), nullable=False)
    constraint = db.Column(db.String(1000), nullable=False)
    solved = db.Column(db.Integer, nullable=False, default=0)
    tried = db.Column(db.Integer, nullable=False , default=0)


class TestCases(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prob_id = db.Column(db.Integer, nullable=False)
    input = db.Column(db.String(10000), nullable=False)
    output = db.Column(db.String(10000), nullable=False)