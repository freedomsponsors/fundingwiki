from django.urls import path, re_path
from apps.issues.views import issue_views

urlpatterns = [
    re_path('(?P<offer_id>\d+)/pay', issue_views.payOfferForm),
    path('pay/submit', issue_views.payOffer),
    path('revoke/submit', issue_views.revokeOffer),
    path('edit/submit', issue_views.editOffer),
]
