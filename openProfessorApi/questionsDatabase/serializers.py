from rest_framework import serializers
from questionsDatabase.models import Question, Answer

class QuestionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Question
        fields = ('id',
                  'text')

class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ('id',
                  'text',
                  'correct',
                  'question')
