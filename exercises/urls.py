from django.urls import path
from . import views

app_name = 'exercises'  # This line sets the namespace for the app

urlpatterns = [
    path('', views.exercise_list, name='exercise_list'),
    path('add/', views.exercise_add, name='exercise_add'),
    
    path('<int:exercise_id>/submit/', views.submit_code, name='submit_code'),
    
    path('result/<int:submission_id>/', views.result_detail, name='result_detail'),
    path('results/', views.result_list, name='result_list'),
    path('run_code/', views.run_code, name='run_code'),
]

