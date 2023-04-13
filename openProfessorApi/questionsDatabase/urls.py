from django.urls import re_path
from questionsDatabase import views

urlpatterns = [
    re_path(r'^api/questions$', views.question_list),
    re_path(r'^api/questions/(?P<pk>[0-9]+)$', views.question_detail),
    re_path(r'^api/courses$', views.courses),
]
