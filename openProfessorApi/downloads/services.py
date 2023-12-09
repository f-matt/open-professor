from flask import request, jsonify, make_response, send_file
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from main import db, app
from parameters.models import Parameter
from questions.models import Question
from answers.models import Answer

import numpy as np
import io
import zipfile
import traceback

class DownloadsService(Resource):
    @jwt_required()
    def get(self):
        print (request)
        course_id = request.args.get("course_id", None)
        section = request.args.get("section", None)

        if not course_id or not section:
            return jsonify(message="Course id and section id are mandatory.")

        moodle_header = Parameter.query.filter_by(name='MOODLE_HEADER').first()
        moodle_mask = Parameter.query.filter_by(name='MOODLE_MASK').first()
        latex_mask = Parameter.query.filter_by(name='LATEX_MASK').first()

        questions = list(Question.query.filter(Question.course_id==course_id, Question.section==section).all())
        np.random.shuffle(questions)
    
        moodle_text = moodle_header.value
        for question in questions[0:10]:
            answers = Answer.query.filter_by(question_id=question.id)
            correct_answer = None
            wrong_answers = list()

            for answer in answers:
                if answer.correct:
                    correct_answer = answer.text
                else:
                    wrong_answers.append(answer.text)

            moodle_text += moodle_mask.value.format('b{0}'.format(section), 
                question.id,
                question.text, 
                correct_answer, 
                wrong_answers[0], 
                wrong_answers[1],
                wrong_answers[2])

        latex_text = ''
        correct_answers = list()
        alternatives = ['A', 'B', 'C', 'D']
        question_number = 1
        for question in questions[10:20]:
            answers = Answer.query.filter_by(question_id=question.id)
            correct_answer = None
            wrong_answers = list()

            for answer in answers:
                if answer.correct:
                    correct_answer = answer.text
                else:
                    wrong_answers.append(answer.text)

            question.text = question.text.replace('__________', '\\rule{5cm}{1pt}')
            correct_answer = correct_answer.replace('<br>', '\n\n')
            correct_answer = correct_answer.replace('<pre>', '\\begin{{lstlisting}}')
            correct_answer = correct_answer.replace('</pre>', '\\end{{lstlisting}}')

            for wrong_answer in wrong_answers:
                wrong_answer = wrong_answer.replace('<br>', '\n\n')
                wrong_answer = wrong_answer.replace('<pre>', '\\begin{{lstlisting}}')
                wrong_answer = wrong_answer.replace('</pre>', '\\end{{lstlisting}}')

            answers = [None, None, None, None]
            idx_correct = np.random.randint(4)
            other_idx = [i for i in range(4) if i != idx_correct]
            answers[idx_correct] = correct_answer
            correct_answers.append(alternatives[idx_correct])

            for i in range(3):
                answers[other_idx[i]] = wrong_answers[i]

            latex_text += latex_mask.value.format(question_number, 
                question.text,
                answers[0], 
                answers[1], 
                answers[2], 
                answers[3])

            question_number += 1

        latex_text += "\\end{document}\n\n"
        latex_text += "% ANSWERS: " + str(correct_answers)

        outfile = io.BytesIO()
        with zipfile.ZipFile(outfile, 'w') as zf:
            zf.writestr("questions.xml", moodle_text)
            zf.writestr("questions.tex", latex_text)

        response = make_response(outfile.getvalue())
        response.headers.set("Content-Type", "application/octet-stream")
        response.headers.set("Content-Disposition", "attachment; filename=files.zip")

        return response

class DownloadLatex(Resource):
    @jwt_required()
    def get(self):
        course_id = request.args.get("course", None)
        section = request.args.get("section", None)

        if not course_id:
            return {"message": "Course id is mandatory.and section id are mandatory."}, 400

        try:
            latex_mask = db.session.execute(db.select(Parameter).where(Parameter.name=="LATEX_MASK")).scalar_one()

            query = db.select(Question)
            if course_id:
                query = query.where(Question.course_id==course_id)
            if section:
                query = query.where(Question.section==section)
            questions = db.session.execute(query).scalars().all()
            np.random.shuffle(questions)

            latex_text = ''
            correct_answers = list()
            alternatives = ['A', 'B', 'C', 'D']
            question_number = 1
            for question in questions[0:10]:
                answers = db.session.execute(db.select(Answer).where(Answer.question_id==question.id)).scalars()
                correct_answer = None
                wrong_answers = list()

                for answer in answers:
                    if answer.correct:
                        correct_answer = answer.text
                    else:
                        wrong_answers.append(answer.text)

                question.text = question.text.replace('__________', '\\rule{5cm}{1pt}')
                correct_answer = correct_answer.replace('<br>', '\n\n')
                correct_answer = correct_answer.replace('<pre>', '\\begin{{lstlisting}}')
                correct_answer = correct_answer.replace('</pre>', '\\end{{lstlisting}}')

                for wrong_answer in wrong_answers:
                    wrong_answer = wrong_answer.replace('<br>', '\n\n')
                    wrong_answer = wrong_answer.replace('<pre>', '\\begin{{lstlisting}}')
                    wrong_answer = wrong_answer.replace('</pre>', '\\end{{lstlisting}}')

                answers = [None, None, None, None]
                idx_correct = np.random.randint(4)
                other_idx = [i for i in range(4) if i != idx_correct]
                answers[idx_correct] = correct_answer
                correct_answers.append(alternatives[idx_correct])

                for i in range(3):
                    answers[other_idx[i]] = wrong_answers[i]

                latex_text += latex_mask.value.format(question_number, 
                    question.text,
                    answers[0], 
                    answers[1], 
                    answers[2], 
                    answers[3])

                question_number += 1

            latex_text += "\\end{document}\n\n"
            latex_text += "% ANSWERS: " + str(correct_answers)

            buffer = io.StringIO()
            buffer.write(latex_text)

            response = make_response(buffer.getvalue())
            response.headers.set("Content-Type", "text/plain;encoding=UTF-8")
            response.headers.set("Content-Disposition", "attachment; filename=questions.tex")
            return response
        except Exception as e:
            app.logger.error(traceback.format_exc())
            return {"message": "Error creating file."}, 400
