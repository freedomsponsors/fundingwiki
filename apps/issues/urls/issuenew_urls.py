from django.urls import path
from apps.issues.views import issue_views
from apps.issues.views import issuenew_views
from apps.issues.views import comment_views
from apps.issues.views import media_views
from apps.issues.views import revision_views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('addSolution', issuenew_views.addSolution),
]