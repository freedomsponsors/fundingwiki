# coding: utf-8
from django.urls import path
from apps.issues.views import feedback_views

urlpatterns = [
    path('', feedback_views.feedback, name='feedback'),
    path('/submit', feedback_views.addFeedback, name='addFeedback'),
]
