from app import db
from app.models import User, Profile, Post
from app.schemas import UserSchema, PostSchema


class UserService:
    def get_by_id(self, user_id):
        user = db.session.query(User).filter(User.id == user_id).first_or_404()
        return user

    def get_by_username(self, username):
        user = db.session.query(User).filter(User.username == username).first_or_404()
        return user

    def create(self, data):
        user = User(username=data.get('username'), email=data.get('email'))
        user.set_password(data.get('password'))

        db.session.add(user)
        db.session.commit()

        profile = Profile(user_id=user.id)
        db.session.add(profile)
        db.session.commit()

        return user

    def update(self, data):
        user = self.get_by_id(data['id'])
        data['profile']['id'] = user.profile.id
        data['profile']['user_id'] = user.id

        user = UserSchema(exclude=('password',)).load(data)
        db.session.add(user)
        db.session.commit()

        return user

    def delete(self, user_id):
        user = self.get_by_id(user_id)
        profile = user.profile
        db.session.delete(profile)
        db.session.commit()

        db.session.delete(user)
        db.session.commit()

        return True


class PostService:
    def get_by_id(self, post_id):
        post = db.session.query(Post).filter(Post.id == post_id).first_or_404()
        return post

    def create(self, data):
        # Add the post to the database
        post = Post(title=data.get('title'), content=data.get('content'), author_id=data.get('author_id'))
        db.session.add(post)
        db.session.commit()
        return post

    def update(self, data):
        post = self.get_by_id(data['id'])
        data['id'] = post.id

        post = PostSchema().load(data)
        db.session.add(post)
        db.session.commit()

        return post

    def delete(self, post_id):
        post = self.get_by_id(post_id)
        db.session.delete(post)
        db.session.commit()

        return True


class UserPostService:
    def get_by_user_id(self, user_id):
        posts = db.session.query(Post).filter(Post.author_id == user_id).all()
        return posts

    def get_by_post_id(self, post_id, user_id):
        post = db.session.query(Post).filter(Post.author_id == user_id, Post.id == post_id).first_or_404()
        return post

    def create(self, data):
        # Add the post to the database
        post = Post(title=data.get('title'), content=data.get('content'), author_id=data.get('author_id'))
        db.session.add(post)
        db.session.commit()
        return post

    def update(self, data):
        post = self.get_by_post_id(post_id=data['id'], user_id=data['author_id'])
        data['id'] = post.id

        post = PostSchema().load(data)
        db.session.add(post)
        db.session.commit()

        return post

    def delete(self, post_id, user_id):
        post = self.get_by_post_id(post_id=post_id, user_id=user_id)
        db.session.delete(post)
        db.session.commit()

        return True
