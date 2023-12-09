# -*- coding:utf-8 -*-
from main import db
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from courses.models import Course

class Question(db.Model):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(String)
    section: Mapped[int] = mapped_column(Integer)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    course: Mapped[Course] = relationship()

    def __repr__(self):
        return f"<Question {self.id}>"
