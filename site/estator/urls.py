"""
URL configuration for estator project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.property_list, name="property_list"),
    path("<int:property_id>/", views.property_detail_ajax, name="property_detail_ajax"),

    path('register/', views.register),
    path('login/', views.login),
    path('register/signup/', views.signup),
    path('login/signin/', views.signin),
    path('logout/', views.logout),

    path('profile/', views.profile, name='profile'),
    path('create_application/', views.create_application, name='create_application'),
    path('delete_application/<int:application_id>/', views.delete_application, name='delete_application'),
    
]
