from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.quiz_list, name='quiz_list'),
    path('create/', views.create_quiz, name='create_quiz'),
    path('<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('<int:quiz_id>/edit/', views.edit_quiz, name='edit_quiz'),
    path('<int:quiz_id>/delete/', views.delete_quiz, name='delete_quiz'),
    path('<int:quiz_id>/submit/', views.submit_quiz, name='submit_quiz'),
    path('submission/<int:submission_id>/result/', views.submission_result, name='submission_result'),
    path('make-question/', views.make_question, name='make_question'),
    path('load-questions/', views.load_questions, name='load_questions'),
]
