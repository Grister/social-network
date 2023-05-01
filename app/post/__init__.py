import click
import pandas as pd
from flask import Blueprint

from config import Config
from ..models import User

bp = Blueprint('post', __name__, url_prefix='/post')

from . import routes  # noqa


@bp.cli.command("extract_posts")
@click.argument('user_id', type=int)
def extract_posts(user_id):
    user = User.query.get_or_404(user_id)
    posts = user.posts.all()

    data = {'Post Title': [post.title for post in posts],
            'Likes count': [len(post.likes) for post in posts],
            'Dislikes count': [len(post.dislikes) for post in posts],
            'Post Created at': [post.created_at for post in posts]}

    df = pd.DataFrame(data)
    output_file_path = Config.BASE_DIR / f"{user.username}_posts.csv"
    df.to_csv(output_file_path, index=False, sep=';')
    print(f'Saved in dir {output_file_path}')
