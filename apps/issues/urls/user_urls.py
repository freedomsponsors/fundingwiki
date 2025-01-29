from django.urls import path, re_path
from apps.issues.views import user_views


urlpatterns = [
    # url(r'^$', 'listUsers'),
    path('edit', user_views.editUserForm, name='editUserForm'),
    path('edit/submit', user_views.editUser, name='editUser'),
    path('cancel_account', user_views.cancel_account),
    re_path(r'^(?P<user_id>\d+)/$', user_views.viewUserById),
    re_path(r'^(?P<user_id>\d+)/(?P<user_slug>.*)$', user_views.viewUserById),
    re_path(r'^(?P<username>.+)/$', user_views.viewUserByUsername),
]
