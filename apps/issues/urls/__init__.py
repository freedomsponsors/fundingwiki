from django.urls import include, path
from django.views.generic import TemplateView, RedirectView
from django.conf import settings
from apps.issues.views import main_views
from apps.issues.views import paypal_views
from apps.issues.views import bitcoin_views
from apps.issues.views import json_views

urlpatterns = [
    path('$', main_views.home),
    path('admail/', main_views.admail),
    path('mailtest/', main_views.mailtest),
    path('about/', RedirectView.as_view(url='http://blog.freedomsponsors.org/about/')),
    path('dev/', RedirectView.as_view(url='/developers/')),
    path('issue', main_views.redirect_core),
]

urlpatterns += [
    path('paypal/cancel', paypal_views.paypalCancel),
    path('paypal/return', paypal_views.paypalReturn),
    # path('paypal/'+settings.PAYPAL_IPNNOTIFY_URL_TOKEN+'', paypal_views.paypalIPN),
]

urlpatterns += [
    # path('bitcoin/'+settings.BITCOIN_IPNNOTIFY_URL_TOKEN+'', bitcoin_views.bitcoinIPN),
]

urlpatterns += [
    path('json/project', json_views.project),
    path('json/translate', json_views.translate),
    path('json/detectLanguage', json_views.detectLanguage),
    path('json/suggestTags', json_views.suggestTags),
    path('json/suggestTagsLocal', json_views.suggestTagsLocal),
    path('json/suggestGeo', json_views.suggestGeo),
    path('json/by_issue_url', json_views.by_issue_url),
    path('json/get_offers', json_views.get_offers),
    path('json/list_issue_cards', json_views.list_issue_cards),
    path('json/add_tag', json_views.add_tag),
    path('json/remove_tag', json_views.remove_tag),
    path('json/latest_activity', json_views.latest_activity),
    path('json/toggle_watch', json_views.toggle_watch),
    path('json/check_username_availability/(?P<username>.+)', json_views.check_username_availability),
]
