from django.urls import path
from . import views

urlpatterns = [
    path('verify/', views.verify, name='verify'),
    path('init/', views.init, name='init')
]
