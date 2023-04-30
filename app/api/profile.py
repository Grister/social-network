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


class ProfileResource(Resource):
    def get(self, profile_id=None):
        profile = profile_service.get_by_id(profile_id)
        return jsonify(ProfileSchema().dump(profile, many=False))

    def put(self, profile_id):
        json_data = request.get_json()
        json_data['id'] = profile_id

        profile = profile_service.update(json_data)
        return jsonify(ProfileSchema().dump(profile, many=False))
