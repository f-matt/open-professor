from django.shortcuts import render
from rest_framework.decorators import api_view

@api_view(['GET', 'POST', 'DELETE'])
def question_list(request):
    print ('question list')
    pass
    # TODO

@api_view(['GET', 'PUT', 'DELETE'])
def question_detail(request, pk):
    try:
        question = Question.objects.get(pk=pk)
    except Question.DoesNotExist:
        return JsonResponse({'message' : 'Question not found.'}, status=status.HTTP_404_NOT_FOUND)
