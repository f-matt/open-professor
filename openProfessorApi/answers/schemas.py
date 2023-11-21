from main import ma
from marshmallow_sqlalchemy import fields

from answers.models import Answer
from questions.schemas import QuestionSchema

class AnswerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Answer
        include_relationships = True
        include_fk = True

    question = fields.Nested(QuestionSchema)
