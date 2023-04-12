from django.db import models

class Question(models.Model):
    text = models.CharField(max_length=500, blank=False)

    class Meta:
        db_table = "questions"


class Answer(models.Model):
    text = models.CharField(max_length=200, blank=False)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.RESTRICT)

    class Meta:
        db_table = "answers"
