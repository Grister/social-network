from flask import Blueprint
import pandas as pd

from config import Config
from ..models import User

bp = Blueprint('user', __name__, url_prefix='/user')

from . import routes  # noqa


@bp.cli.command('exctract_users')
def exctract_users():
    users = User.query.all()

    data = {'username': [user.username for user in users],
            'email': [user.email for user in users],
            'full_name': [user.profile.full_name for user in users],
            'post_count': [user.posts.count() for user in users]}

    df = pd.DataFrame(data)
    output_file_path = Config.BASE_DIR / 'users.csv'
    df.to_csv(output_file_path, sep=';', index=False)
    print(f'Saved in dir {output_file_path}')
