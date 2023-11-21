# -*- coding:utf-8 -*-
from main import db

class Parameter(db.Model):
    __tablename__ = "parameters"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    value = db.Column(db.String)

    def __repr__(self):
        return f"<Parameter {self.id}>"
