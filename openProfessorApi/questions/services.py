from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from main import app, db
from questions.models import Question
from answers.models import Answer

import traceback

class QuestionsService(Resource):
    @jwt_required()
    def post(self):
        question_text = request.json.get("question", None)
        correct_answer_text = request.json.get("correct", None)
        wrong_answer_1_text = request.json.get("wrong1", None)
        wrong_answer_2_text = request.json.get("wrong2", None)
        wrong_answer_3_text = request.json.get("wrong3", None)
        course_id = request.json.get("course_id", None)

        if not question_text or not correct_answer_text or not wrong_answer_1_text \
            or not wrong_answer_2_text or not wrong_answer_3_text or not course_id:

            return jsonify({"message": "Question text, answers and course are required."}), 401

        try:
            question = Question()
            question.text = question_text
            question.course_id = course_id
            db.session.add(question)
            db.session.flush()

            answer1 = Answer()
            answer1.text = correct_answer_text
            answer1.correct = True
            answer1.question_id = question.id
            db.session.add(answer1)

            answer2 = Answer()
            answer2.text = wrong_answer_1_text
            answer2.correct = False
            answer2.question_id = question.id
            db.session.add(answer2)

            answer3 = Answer()
            answer3.text = wrong_answer_2_text
            answer3.correct = False
            answer3.question_id = question.id
            db.session.add(answer3)

            answer4 = Answer()
            answer4.text = wrong_answer_3_text
            answer4.correct = False
            answer4.question_id = question.id
            db.session.add(answer4)

            db.session.commit()

            return "", 200
        except Exception as e:
            app.logger.error(traceback.format_exc())
            return jsonify({"message": "Error inserting new question."})
