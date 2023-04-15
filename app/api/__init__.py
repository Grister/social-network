from flask import Blueprint
from flask_restful import Api
from .user import UsersResource, UserResource
from .post import PostsResource, PostResource
from .users_post import UserPostsResource, UserPostResource
from .profile import ProfilesResource, ProfileResource
from .like import LikeResource, LikesResource
from .dislake import DislikesResource, DislikeResource

bp = Blueprint('api', __name__, url_prefix="/api")
api = Api(bp)

api.add_resource(UsersResource, '/users', endpoint="users_list")
api.add_resource(UserResource, '/users/<int:user_id>', endpoint="user_details")

api.add_resource(PostsResource, '/posts', endpoint="posts_list")
api.add_resource(PostResource, '/posts/<int:post_id>', endpoint="post_details")

api.add_resource(UserPostsResource, '/users/<int:user_id>/posts', endpoint="user_posts_list")
api.add_resource(UserPostResource, '/users/<int:user_id>/posts/<int:post_id>', endpoint="user_post_details")

api.add_resource(ProfilesResource, '/profiles', endpoint="profiles_list")
api.add_resource(ProfileResource, '/profiles/<int:profile_id>', endpoint="profile_details")

api.add_resource(LikesResource, '/likes', endpoint="likes_list")
api.add_resource(LikeResource, '/likes/<int:like_id>', endpoint="like_details")

api.add_resource(DislikesResource, '/dislikes', endpoint="dislikes_list")
api.add_resource(DislikeResource, '/dislikes/<int:dislike_id>', endpoint="dislike_details")
