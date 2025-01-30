# coding: utf-8
from django.urls import path
from apps.issues.views import api_views

urlpatterns = [
    path('project/(?P<project_id>\d+)', api_views.get_project),
    path('login', api_views.login),
    path('logout', api_views.logout),
    path('whoami', api_views.whoami),
    path('list_issues', api_views.list_issues),
]
