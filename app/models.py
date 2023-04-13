from datetime import datetime
from hashlib import md5

from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)


# Followers model
class Follower(BaseModel):
    __tablename__ = "followers"
    follower_id = db.Column('follower_id', db.Integer, db.ForeignKey('user.id'))
    followed_id = db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, index=True)
    email = db.Column(db.String, unique=True, index=True)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    posts = db.relationship(
        "Post", backref="author", uselist=True, lazy="dynamic", cascade="all,delete"
    )
    likes = db.relationship(
        'Like', backref='user', lazy='dynamic', primaryjoin='User.id==Like.user_id', cascade="all,delete"
    )
    dislikes = db.relationship(
        'Dislike', backref='user', lazy='dynamic', primaryjoin='User.id==Dislike.user_id', cascade="all,delete"
    )

    # Відношення до таблиці "followers"
    user_followee = db.relationship('User',
                                     secondary='followers',
                                     primaryjoin=(Follower.follower_id == id),
                                     secondaryjoin=(Follower.followed_id == id),
                                     backref=db.backref('followers', lazy='dynamic'),
                                     lazy='dynamic')

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    def set_password(self, password):
        """
        Set user password hash
        """
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """
        Check user password hash with existing in db
        """
        return check_password_hash(self.password, password)

    def follow(self, user_id):
        if not self.is_following(user_id):
            subscription = Follower(follower_id=self.id, followed_id=user_id)
            db.session.add(subscription)
            db.session.commit()

    def unfollow(self, user_id):
        subscription = Follower.query.filter_by(follower_id=self.id, followed_id=user_id).first()
        if subscription:
            db.session.delete(subscription)
            db.session.commit()

    def is_following(self, user_id):
        return self.user_followee.filter_by(id=user_id).first() is not None

    def __repr__(self):
        return f"{self.username}({self.email})"


class Profile(BaseModel):
    __tablename__ = "profiles"
    __table_args__ = (
        db.Index("idx_profiles_user_id", "user_id"),
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", name="fk_profiles_user_id", ondelete="CASCADE"),
        nullable=False
    )
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    bio = db.Column(db.String)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    facebook = db.Column(db.String)
    linkedin = db.Column(db.String)

    user = db.relationship("User", backref=db.backref("profile", uselist=False), uselist=False)


class Post(BaseModel):
    __tablename__ = 'posts'

    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", name="fk_posts_author_id", ondelete="CASCADE"),
        nullable=False
    )

    likes = db.relationship("Like", backref="post", uselist=True, cascade="all,delete")
    dislikes = db.relationship("Dislike", backref="post", uselist=True, cascade="all,delete")


# Like model
class Like(BaseModel):
    __tablename__ = "likes"

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', name="fk_likes_user_id"),
        nullable=False
    )
    post_id = db.Column(
        db.Integer,
        db.ForeignKey('posts.id', name="fk_likes_post_id"),
        nullable=False
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# Dislike model
class Dislike(BaseModel):
    __tablename__ = "dislikes"
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', name="fk_dislikes_user_id"),
        nullable=False
    )
    post_id = db.Column(
        db.Integer,
        db.ForeignKey('posts.id', name="fk_dislikes_post_id"),
        nullable=False
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
