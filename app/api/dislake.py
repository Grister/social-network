from flask_restful import Resource
from flask import jsonify, request
from app import db
from app.schemas import DislikeSchema
from app.models import Dislike
from app.services import DislikeService

dislike_service = DislikeService()


class DislikesResource(Resource):
    def get(self):
        dislike = db.session.query(Dislike).all()
        return jsonify(DislikeSchema().dump(dislike, many=True))

    def post(self):
        json_data = request.get_json()
        dislike = dislike_service.create(json_data)
        response = jsonify(DislikeSchema().dump(dislike, many=False))
        response.status_code = 201
        return response


class DislikeResource(Resource):
    def get(self, dislike_id=None):
        dislike = dislike_service.get_by_id(dislike_id)
        return jsonify(DislikeSchema().dump(dislike, many=False))

    def put(self, dislike_id):
        json_data = request.get_json()
        json_data['id'] = dislike_id

        dislike = dislike_service.update(json_data)
        return jsonify(DislikeSchema().dump(dislike, many=False))

    def delete(self, dislike_id):
        status = dislike_service.delete(dislike_id)
        return jsonify(status=status)
