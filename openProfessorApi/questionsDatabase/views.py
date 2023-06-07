import io
import json 
import zipfile
import numpy as np

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view

from .models import Course, Question, Answer, Parameter

@api_view(['POST'])
def question_list(request):
    if request.method == "POST":
        data = json.loads(request.body)

        course_id = data["course_id"]
        course = Course.objects.get(pk=course_id)

        question = Question()
        question.text = data["question"]
        question.course = course
        question.save()

        correct_answer = Answer()
        correct_answer.text = data["correct"]
        correct_answer.correct = True
        correct_answer.question = question
        correct_answer.save()

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

@api_view(['GET', 'PUT', 'DELETE'])
def question_detail(request, pk):
    try:
        question = Question.objects.get(pk=pk)
    except Question.DoesNotExist:
        return JsonResponse({'message' : 'Question not found.'}, status=JsonResponse.status_code.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def questions_by_course(request, pk):
    try:
        questions = Question.objects.filter(course__id=pk).all()
        ids = list()
        for question in questions:
            ids.append(question.id)
        np.random.shuffle(ids)
        return JsonResponse({'questions' : ids})
    except Exception as e:
        print (e)
        return JsonResponse({'message' : 'Error retrieving questions.'}, status=404)


@api_view(["GET", "POST"])
def courses(request):
    if request.method == "POST":
      data = json.loads(request.body)

      course = Course()
      course.name = data["name"]
      course.save()

      return JsonResponse({"status" : "ok"})
    elif request.method == "GET":
      courses = Course.objects.all().values()

      return JsonResponse({'courses' : list(courses)})

@api_view(['GET'])
def download_moodle(request, ids_str):
    moodle_header = Parameter.objects.filter(name='MOODLE_HEADER').values()
    moodle_mask = Parameter.objects.filter(name='MOODLE_MASK').values()
    ids = map(int, ids_str.split(','))
    questions = Question.objects.filter(id__in=ids)
    text = moodle_header.value
    for question in questions:
        answers = Answer.objects.filter(question__id=question.id)
        correct_answer = None
        wrong_answers = list()

        for answer in answers:
            if answer.correct:
                correct_answer = answer.text
            else:
                wrong_answers.append(answer.text)

        text += moodle_mask.value.format('b02', 
            question.id,
            question.text, 
            correct_answer, 
            wrong_answers[0], 
            wrong_answers[1],
            wrong_answers[2])

    response = HttpResponse(text, content_type='text/plain; charset=UTF-8')
    response['Content-Disposition'] = ('attachment; filename=questions.xml')

    return response

@api_view(['GET'])
def download_latex(request, ids_str):
    latex_mask = Parameter.objects.filter(name='LATEX_MASK').values()
    ids = map(int, ids_str.split(','))
    questions = Question.objects.filter(id__in=ids)
    text = ''
    correct_answers = list()
    alternatives = ['A', 'B', 'C', 'D']
    question_number = 1
    for question in questions:
        answers = Answer.objects.filter(question__id=question.id)
        correct_answer = None
        wrong_answers = list()

        for answer in answers:
            if answer.correct:
                correct_answer = answer.text
            else:
                wrong_answers.append(answer.text)

        question.text = question.text.replace('__________', '\\rule{5cm}{1pt}')
        correct_answer = correct_answer.replace('<br>', '\n\n')
        correct_answer = correct_answer.replace('<pre>', '\\begin{{lstlisting}}')
        correct_answer = correct_answer.replace('</pre>', '\\end{{lstlisting}}')

        for wrong_answer in wrong_answers:
            wrong_answer = wrong_answer.replace('<br>', '\n\n')
            wrong_answer = wrong_answer.replace('<pre>', '\\begin{{lstlisting}}')
            wrong_answer = wrong_answer.replace('</pre>', '\\end{{lstlisting}}')

        answers = [None, None, None, None]
        idx_correct = np.random.randint(4)
        other_idx = [i for i in range(4) if i != idx_correct]
        answers[idx_correct] = correct_answer
        correct_answers.append(alternatives[idx_correct])

        for i in range(3):
            answers[other_idx[i]] = wrong_answers[i]

        text += latex_mask.format(question_number, 
            question.text,
            answers[0], 
            answers[1], 
            answers[2], 
            answers[3])

        question_number += 1

    text += "\\end{document}\n\n"
    text += "% ANSWERS: " + str(correct_answers)

    response = HttpResponse(text, content_type='text/plain; charset=UTF-8')
    response['Content-Disposition'] = ('attachment; filename=questions.tex')

    return response

@api_view(['GET'])
def download_all(request, course_id):
    moodle_header = Parameter.objects.filter(name='MOODLE_HEADER').values()[0]
    moodle_mask = Parameter.objects.filter(name='MOODLE_MASK').values()[0]
    latex_mask = Parameter.objects.filter(name='LATEX_MASK').values()[0]

    questions = list(Question.objects.filter(course__id=course_id).values())
    np.random.shuffle(questions)
 
    moodle_text = moodle_header['value']
    for question in questions[0:10]:
        answers = Answer.objects.filter(question__id=question['id'])
        correct_answer = None
        wrong_answers = list()

        for answer in answers:
            if answer.correct:
                correct_answer = answer.text
            else:
                wrong_answers.append(answer.text)

        moodle_text += moodle_mask['value'].format('b02', 
            question['id'],
            question['text'], 
            correct_answer, 
            wrong_answers[0], 
            wrong_answers[1],
            wrong_answers[2])

    latex_text = ''
    correct_answers = list()
    alternatives = ['A', 'B', 'C', 'D']
    question_number = 1
    for question in questions[10:20]:
        answers = Answer.objects.filter(question__id=question['id'])
        correct_answer = None
        wrong_answers = list()

        for answer in answers:
            if answer.correct:
                correct_answer = answer.text
            else:
                wrong_answers.append(answer.text)

        question['text'] = question['text'].replace('__________', '\\rule{5cm}{1pt}')
        correct_answer = correct_answer.replace('<br>', '\n\n')
        correct_answer = correct_answer.replace('<pre>', '\\begin{{lstlisting}}')
        correct_answer = correct_answer.replace('</pre>', '\\end{{lstlisting}}')

        for wrong_answer in wrong_answers:
            wrong_answer = wrong_answer.replace('<br>', '\n\n')
            wrong_answer = wrong_answer.replace('<pre>', '\\begin{{lstlisting}}')
            wrong_answer = wrong_answer.replace('</pre>', '\\end{{lstlisting}}')

        answers = [None, None, None, None]
        idx_correct = np.random.randint(4)
        other_idx = [i for i in range(4) if i != idx_correct]
        answers[idx_correct] = correct_answer
        correct_answers.append(alternatives[idx_correct])

        for i in range(3):
            answers[other_idx[i]] = wrong_answers[i]

        latex_text += latex_mask['value'].format(question_number, 
            question['text'],
            answers[0], 
            answers[1], 
            answers[2], 
            answers[3])

        question_number += 1

    latex_text += "\\end{document}\n\n"
    latex_text += "% ANSWERS: " + str(correct_answers)

    outfile = io.BytesIO()
    with zipfile.ZipFile(outfile, 'w') as zf:
        zf.writestr("questions.xml", moodle_text)
        zf.writestr("questions.tex", latex_text)

    response = HttpResponse(outfile.getvalue(), content_type='application/octet-stream')
    response['Content-Disposition'] = ('attachment; filename=files.zip')

    return response
