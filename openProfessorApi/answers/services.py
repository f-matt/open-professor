from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from main import app, db
from answers.models import Answer

import traceback

class AnswersService(Resource):
    @jwt_required()
    def post(self):
        text = request.json.get("text", None)
        correct = request.json.get("correct", None)
        question_id = request.json.get("question_id", None)
        if not text or not question_id:
            return jsonify({"message": "Answer text and question are required."}), 401

        try:
            answer = Answer()
            answer.text = text
            answer.correct = correct
            answer.question_id = question_id

            db.session.add(answer)
            db.session.commit()

            return "", 200
        except Exception as e:
            app.logger.error(traceback.format_exc())
            return jsonify({"message": "Error inserting new answer."})
