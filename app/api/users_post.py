from flask_restful import Resource
from flask import jsonify, request
from app.schemas import PostSchema
from app.services import UserPostService

post_service = UserPostService()


class UserPostsResource(Resource):
    def get(self, user_id=None):
        post = post_service.get_by_user_id(user_id)
        return jsonify(PostSchema().dump(post, many=True))

    def post(self, user_id):
        json_data = request.get_json()
        json_data['author_id'] = user_id
        post = post_service.create(json_data)
        response = jsonify(PostSchema().dump(post, many=False))
        response.status_code = 201
        return response


class UserPostResource(Resource):
    def get(self, post_id=None, user_id=None):
        post = post_service.get_by_post_id(post_id, user_id)
        return jsonify(PostSchema().dump(post, many=False))

    def put(self, user_id, post_id):
        json_data = request.get_json()
        json_data['author_id'] = user_id
        json_data['id'] = post_id

        user = post_service.update(json_data)
        return jsonify(PostSchema().dump(user, many=False))

    def delete(self, user_id, post_id):
        status = post_service.delete(user_id=user_id, post_id=post_id)
        return jsonify(status=status)
