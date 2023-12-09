from flask import jsonify, request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from sqlalchemy import func, text
from main import app, db
from auth.models import User

from base64 import b64encode
from hashlib import sha256

import traceback

class LoginService(Resource):
    def post(self):
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        if not username or not password:
            return jsonify({"message": "Username and password required."}), 401

        try:
            query = db.select(User).where(User.username.ilike(username))
            user = db.session.execute(query).one_or_none()[0]

            if not user:
                return jsonify({"message": "Invalid username/password."}), 401

            s = sha256()
            s.update(password.encode("ascii"))
            encoded = b64encode(s.digest()).decode("ascii")

            if encoded == user.password:
                permissions = list()
                for r in user.roles:
                    for p in r.permissions:
                        permissions.append(p.description)

                access_token = create_access_token(identity=username, additional_claims={"permissions": permissions})
                refresh_token = create_refresh_token(identity=username)

                return jsonify(access_token=access_token, refresh_token=refresh_token)
        except Exception as e:
            app.logger.error(traceback.format_exc())

        return {"message": "Error processing authentication."}, 400

class RefreshService(Resource):
    @jwt_required(refresh=True)
    def post(self):
        try:
            identity = get_jwt_identity()
            access_token = create_access_token(identity=identity)
            return jsonify(access_token=access_token)
        except Exception as e:
            app.logger.error(traceback.format_exc())

        return jsonify({"message": "Error refreshing token."})
