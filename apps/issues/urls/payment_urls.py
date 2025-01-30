from django.urls import path
from apps.issues.views import payment_views

urlpatterns = [
    path('', payment_views.list_payments),
    path('(?P<payment_id>\d+)/', payment_views.view_payment),
]
