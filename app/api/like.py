from flask_restful import Resource
from flask import jsonify, request
from app import db
from app.schemas import LikeSchema
from app.models import Like
from app.services import LikeService

like_service = LikeService()


class LikesResource(Resource):
    def get(self):
        likes = db.session.query(Like).all()
        return jsonify(LikeSchema().dump(likes, many=True))

    def post(self):
        json_data = request.get_json()
        like = like_service.create(json_data)
        response = jsonify(LikeSchema().dump(like, many=False))
        response.status_code = 201
        return response


class LikeResource(Resource):
    def get(self, like_id=None):
        user = like_service.get_by_id(like_id)
        return jsonify(LikeSchema().dump(user, many=False))

    def put(self, like_id):
        json_data = request.get_json()
        json_data['id'] = like_id

        like = like_service.update(json_data)
        return jsonify(LikeSchema().dump(like, many=False))

    def delete(self, like_id):
        status = like_service.delete(like_id)
        return jsonify(status=status)
