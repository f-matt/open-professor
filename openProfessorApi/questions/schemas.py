from main import ma
from marshmallow_sqlalchemy import fields

from questions.models import Question
from courses.schemas import CourseSchema

class QuestionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Question
        include_relationships = True
        include_fk = True

    course = fields.Nested(CourseSchema)
