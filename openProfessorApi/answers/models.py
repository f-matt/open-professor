# -*- coding:utf-8 -*-
from main import db

class Answer(db.Model):
    __tablename__ = "answers"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    correct = db.Column(db.Boolean)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    question = db.relationship("Question")

    def __repr__(self):
        return f"<Answer {self.id}>"
