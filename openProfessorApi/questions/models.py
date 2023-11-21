# -*- coding:utf-8 -*-
from main import db

class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String())
    section = db.Column(db.Integer)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    course = db.relationship("Course")

    def __repr__(self):
        return f"<Question {self.id}>"
