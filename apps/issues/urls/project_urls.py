from django.urls import path, re_path
from apps.issues.views import project_views


urlpatterns = [
    path('', project_views.list),
    re_path('(?P<project_id>\d+)/', project_views.view),
    re_path('(?P<project_id>\d+)/edit', project_views.edit_form),
    re_path('(?P<project_name>.+)/edit', project_views.edit_form),
    re_path('(?P<project_name>.+)/', project_views.view),
    re_path('(?P<project_id>\d+)/.*', project_views.view),
    path('submit', project_views.edit, name='edit_project'),
]
