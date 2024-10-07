"""
URL configuration for LMS_SYSTEM project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.contrib import admin
from django.urls import path, include
from .views import home_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),  # Define a home URL pattern
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('', include('main.urls')),  # Include the URLs of the main app

    path('module_group/', include('module_group.urls')),  
    path('user/', include(('user.urls', 'user'), namespace='user')),  # Register user app URLs with a namespace
    
     # Add this to include Django's built-in authentication views
    # path('accounts/', include('django.contrib.auth.urls')),
    # path('accounts/', include(('user.urls', 'user'), namespace='user')),
    path('category/', include('category.urls')),  
    path('question/', include('question.urls')),  
    path('subject/', include('subject.urls')), 
    path('quiz/', include('quiz.urls')),  

    path('exercises/', include('exercises.urls')), 
    path('coding_exercise/', include('coding_exercise.urls')), 
    path('student/', include('student.urls')),
]

