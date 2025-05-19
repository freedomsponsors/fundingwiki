from django.urls import path, re_path
from apps.issues.views import user_views
from apps.issues.views import vue_views_api
from apps.issues.views.vue_views_api import *

urlpatterns = [
    path('ideas', Ideas.as_view()),
    path('ideas_import', IdeasImport.as_view()),
    path('ideas_interested', IdeasInterested.as_view()),
    path('ideas_my', IdeasMine.as_view()),
    path('ideas_similar', IdeasSimilar.as_view()),
    path('user', User.as_view()),
    path('idea_vote', vue_views_api.idea_vote),
    path('get_idea_by_id', vue_views_api.get_idea_by_id),
]
