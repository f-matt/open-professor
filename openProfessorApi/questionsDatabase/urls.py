from django.urls import re_path
from questionsDatabase import views

urlpatterns = [
    re_path(r'^api/questions$', views.question_list),
    re_path(r'^api/questions/(?P<pk>[0-9]+)$', views.question_detail),
    re_path(r'^api/questions/course/(?P<pk>[0-9]+)$', views.questions_by_course),
    re_path(r'^api/courses$', views.courses),
    re_path(r'^api/download-moodle/(?P<ids>)$', views.download_moodle),
    re_path(r'^api/download-latex/(?P<ids>)$', views.download_latex),
    re_path(r'^api/download-all/(?P<course_id>[0-9]+)$', views.download_all),
]
