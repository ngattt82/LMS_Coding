from django.urls import path
from . import views

app_name = 'coding_exercise'
urlpatterns = [
    path('', views.exercise_list, name='exercise_list'),
    path('create/', views.exercise_add, name='exercise_add'),
    path('<int:exercise_id>/', views.exercise_detail, name='exercise_detail'),
    path('<int:exercise_id>/edit/', views.exercise_edit, name='exercise_edit'),
    path('exercise/<int:exercise_id>/delete/', views.exercise_delete, name='exercise_delete'),
]
