from flask_restful import Resource
from flask import jsonify, request
from app import db
from app.schemas import ProfileSchema
from app.models import Profile
from app.services import ProfileService

profile_service = ProfileService()


class ProfilesResource(Resource):
    def get(self):
        profiles = db.session.query(Profile).all()
        return jsonify(ProfileSchema().dump(profiles, many=True))

    def post(self):
        json_data = request.get_json()
        profile = profile_service.create(json_data)
        response = jsonify(ProfileSchema().dump(profile, many=False))
        response.status_code = 201
        return response


class ProfileResource(Resource):
    def get(self, profile_id=None):
        profile = profile_service.get_by_id(profile_id)
        return jsonify(ProfileSchema().dump(profile, many=False))

    def put(self, profile_id):
        json_data = request.get_json()
        json_data['id'] = profile_id

        profile = profile_service.update(json_data)
        return jsonify(ProfileSchema().dump(profile, many=False))

    def delete(self, profile_id):
        status = profile_service.delete(profile_id)
        return jsonify(status=status)
