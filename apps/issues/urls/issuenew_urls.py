from django.conf.urls import url
from core.views import issue_views
from core.views import issuenew_views
from core.views import comment_views
from core.views import media_views
from core.views import revision_views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^addSolution$', issuenew_views.addSolution),
]