from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path ('novels/<int:id>', views.novel, name='novels'),
    path('novels/<int:id>/chapter/<int:num>/', views.chapter, name='chapter'),
]
