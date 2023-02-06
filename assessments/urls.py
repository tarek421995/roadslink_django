from django.urls import path, re_path

from assessments import pdfviews
from . import views

app_name = 'assessments'


urlpatterns = [
    path('', views.test_list, name='test_list'),
    path('<int:test_id>/', views.question_list, name='question_list'),
    # path('questions/submit/', views.english_questions, name='english_questions'),
    path('psycometric_test/',
         views.psycometric_tests, name='psycometric_test'),
    path('psycometric_test/<int:psyco_id>/',
         views.psycometric_tests_detail, name='psycometric_tests_detail'),
    path('evaluate_psycometric_test/',
         views.evaluate_psycometric_test, name='evaluate_psycometric_test'),
     path('generate_pdf/<int:user_id>/', pdfviews.generate_pdf, name='generate_pdf'),
    path('results/', views.results, name='results'),
     path('audio', views.audio_qustion, name='audio'),
     path('text', views.text_qustion, name='text'),
     
    path('questions/<int:question_id>/',
         views.question_detail, name='question_detail'),
]
