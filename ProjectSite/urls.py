from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_home, name="home"),
    path('about', views.view_about, name="about"),
]