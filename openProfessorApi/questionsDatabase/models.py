from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=200, blank=False)

    class Meta:
        db_table = "courses"


class Question(models.Model):
    text = models.CharField(max_length=500, blank=False)
    course = models.ForeignKey(Course, on_delete=models.RESTRICT)

    class Meta:
        db_table = "questions"


class Answer(models.Model):
    text = models.CharField(max_length=200, blank=False)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.RESTRICT)

    class Meta:
        db_table = "answers"


class Parameter(models.Model):
    name = models.CharField(max_length=20, blank=False)
    value = models.TextField(blank=False)

    class Meta:
        db_table = "parameters"