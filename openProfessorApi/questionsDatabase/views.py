import json 

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view

from .models import Question, Answer

MASK = '''<question type="multichoice">
    <name>
      <text>b01-{0}</text>
    </name>
    <questiontext format="html">
      <text><![CDATA[<p dir="ltr">{1}</p>]]></text>
    </questiontext>
    <generalfeedback format="html">
      <text></text>
    </generalfeedback>
    <defaultgrade>1.0000000</defaultgrade>
    <penalty>0.0000000</penalty>
    <hidden>0</hidden>
    <idnumber></idnumber>
    <single>true</single>
    <shuffleanswers>true</shuffleanswers>
    <answernumbering>abc</answernumbering>
    <showstandardinstruction>0</showstandardinstruction>
    <correctfeedback format="html">
      <text>Sua resposta está correta.</text>
    </correctfeedback>
    <partiallycorrectfeedback format="html">
      <text>Sua resposta está parcialmente correta.</text>
    </partiallycorrectfeedback>
    <incorrectfeedback format="html">
      <text>Sua resposta está incorreta.</text>
    </incorrectfeedback>
    <shownumcorrect/>
    <answer fraction="100" format="html">
      <text><![CDATA[<p dir="ltr" style="text-align: left;">{2}<br></p>]]></text>
      <feedback format="html">
        <text></text>
      </feedback>
    </answer>
    <answer fraction="0" format="html">
      <text><![CDATA[<p dir="ltr" style="text-align: left;">{3}<br></p>]]></text>
      <feedback format="html">
        <text></text>
      </feedback>
    </answer>
    <answer fraction="0" format="html">
      <text><![CDATA[<p dir="ltr" style="text-align: left;">{4}<br></p>]]></text>
      <feedback format="html">
        <text></text>
      </feedback>
    </answer>
    <answer fraction="0" format="html">
      <text><![CDATA[<p dir="ltr" style="text-align: left;">{5}<br></p>]]></text>
      <feedback format="html">
        <text></text>
      </feedback>
    </answer>
  </question>'''

@api_view(['GET', 'POST', 'DELETE'])
def question_list(request):
    if request.method == "POST":
        data = json.loads(request.body)

        question = Question()
        question.text = data["question"]
        question.save()

        correct_answer = Answer()
        correct_answer.text = data["correct"]
        correct_answer.correct = True
        correct_answer.question = question
        correct_answer.save();

        wrong_answer1 = Answer()
        wrong_answer1.text = data["wrong1"]
        wrong_answer1.correct = False
        wrong_answer1.question = question
        wrong_answer1.save()

        wrong_answer2 = Answer()
        wrong_answer2.text = data["wrong2"]
        wrong_answer2.correct = False
        wrong_answer2.question = question
        wrong_answer2.save()

        wrong_answer3 = Answer()
        wrong_answer3.text = data["wrong3"]
        wrong_answer3.correct = False
        wrong_answer3.question = question
        wrong_answer3.save()

        return JsonResponse({"status" : "ok"})
    elif request.method == "GET":
        questions = Question.objects.all()
        text = ''
        for question in questions:
            answers = Answer.objects.filter(question__id=question.id)
            correct_answer = None
            wrong_answers = list()

            for answer in answers:
                if answer.correct:
                    correct_answer = answer.text
                else:
                    wrong_answers.append(answer.text)

            text += MASK.format(question.id,
                question.text, 
                correct_answer, 
                wrong_answers[0], 
                wrong_answers[1],
                wrong_answers[2])

        response = HttpResponse(text, content_type='text/plain; charset=UTF-8')
        response['Content-Disposition'] = ('attachment; filename=questions.xml')

        return response

@api_view(['GET', 'PUT', 'DELETE'])
def question_detail(request, pk):
    try:
        question = Question.objects.get(pk=pk)
    except Question.DoesNotExist:
        return JsonResponse({'message' : 'Question not found.'}, status=status.HTTP_404_NOT_FOUND)
