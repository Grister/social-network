import click
from flask import Blueprint
from faker import Faker

from app import db
from app.models import User, Post, Profile

bp = Blueprint('fake', __name__)
faker = Faker()


@bp.cli.command("users")
@click.argument('num', type=int)
def users(num):
    """
    Create 'num' of fake users
    """
    for i in range(num):
        username = faker.user_name()
        email = faker.email()
        password = faker.password(length=10)

        first_name, last_name = faker.name().split()[:2]
        facebook_url = f'https://www.facebook.com/{username}'
        linkedin_url = f'https://www.linkedin.com/in/{username}'
        # get user by username & email
        user = (
            db.session.query(User)
            .filter(
                User.username == username,
                User.email == email
            )
        ).first()

        # no such user in db yet --> insert
        if not user:
            user = User(username=username,
                        email=email)

            user.set_password(password)
            db.session.add(user)
            db.session.commit()

            profile = Profile(user_id=user.id,
                              first_name=first_name,
                              last_name=last_name,
                              facebook=facebook_url,
                              linkedin=linkedin_url)
            db.session.add(profile)
            db.session.commit()
            db.session.add(user)

    db.session.commit()
    print(num, 'users added.')


@bp.cli.command("user_posts")
@click.argument('user_id', type=int)
@click.argument('num', type=int)
def user_posts(user_id, num):
    """
    Create the given number of fake posts, assigned to random users
    """

    user = (
        db.session.query(User)
        .filter(User.id == user_id)
    ).first_or_404()

    for i in range(num):
        created_at = faker.date_time_this_year()
        post = Post(
            title=f"Post at {str(created_at)}",
            content=faker.paragraph(),
            author=user,
            created_at=created_at
        )
        db.session.add(post)
    db.session.commit()
    print(num, 'posts added.')
