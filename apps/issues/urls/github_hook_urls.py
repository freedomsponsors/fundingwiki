from django.urls import path
from apps.issues.views import github_hook_views

urlpatterns = [
    path('(?P<token>\w+)/', github_hook_views.hook),
]
