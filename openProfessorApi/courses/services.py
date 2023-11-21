from flask_restful import Resource
from flask_jwt_extended import jwt_required

from main import app
from courses.models import Course
from courses.schemas import CourseSchema

import traceback

class CoursesService(Resource):
    @jwt_required()
    def get(self):
        try:
            courses = Course.query.order_by(Course.name).all()
            schema = CourseSchema(many=True)
            return schema.dump(courses), 200
        except Exception as e:
            app.logger.error(traceback.format_exc())
