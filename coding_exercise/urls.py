from django.urls import path
from . import views

app_name = 'coding_exercise'
urlpatterns = [
    path('', views.exercise_list, name='exercise_list'),
    path('add/', views.exercise_add, name='exercise_add'),
    path('<int:exercise_id>/', views.exercise_detail, name='exercise_detail'),
    path('<int:exercise_id>/edit/', views.exercise_edit, name='exercise_edit'),
    path('exercise/<int:exercise_id>/delete/', views.exercise_delete, name='exercise_delete'),


    path('student/', views.exercise_list_student, name='exercise_list_student'),
    path('student/<int:exercise_id>/', views.exercise_detail_student, name='exercise_detail_student'),
    path('<int:exercise_id>/submit/', views.submit_code, name='submit_code'),
    path('result/<int:submission_id>/', views.result_detail, name='result_detail'),
    path('results/', views.result_list, name='result_list'),
    path('run_code/', views.run_code, name='run_code'),
]
