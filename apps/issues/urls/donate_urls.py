from django.urls import path, re_path
from apps.issues.views import donate_views

urlpatterns = [
    path('', donate_views.donate, name='donate'),
]
