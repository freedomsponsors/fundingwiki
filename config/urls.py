"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import django.contrib.auth.views
from django.contrib import admin
from django.urls import path
from apps.issues.views import issue_views
from django.urls import include
from apps.issues import urls as core_urls
import apps.issues.urls.issue_urls
import apps.issues.urls.user_urls
import apps.issues.urls.solution_urls
import apps.issues.urls.project_urls
import apps.issues.urls.issuenew_urls
import apps.issues.urls.github_hook_urls
import apps.issues.urls.feedback_urls
import apps.issues.urls.payment_urls
import apps.issues.urls.offer_urls
import apps.issues.urls.api_urls
import apps.issues.urls.donate_urls
import apps.issues.urls.vue_api
from apps.issues.views import main_views
from django.views.generic import TemplateView
from apps.issues.views import user_views
import registration.backends.default.urls
import registration.backends.simple.urls
from apps.issues.views import vue_views

from config import settings
from django.conf.urls.static import static

# from registration.backends.default.views import RegistrationView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('issue_submit', issue_views.addIssueForm),
    path('core/', include(core_urls)),
    path('issue/', include(core_urls.issue_urls)),
    path('issues', issue_views.issue_search, name='issue_search'),
    path('issuesvue', issue_views.issue_search_vue),
    path('issuesvue_language', issue_views.issue_search_language),
    path('user/', include(core_urls.user_urls)),

    #vue url
    path('vuedev', TemplateView.as_view(template_name='vue/dev.html')),
    path('', TemplateView.as_view(template_name='vue/index.html')),
    path('vueapi/', include(core_urls.vue_api)),

    #old
    path('solution/', include(core_urls.solution_urls)),
    path('donate/', include(core_urls.donate_urls)),
    # path('logout', django.contrib.auth.views.LogoutView.as_view(), {'next_page': '/'}),
    # path('', include(django.contrib.auth.urls)),
    path('login/', main_views.login),
    path('logout', main_views.logout),

    # path('paypal/', include(paypal.standard.ipn.urls)),
    # path('paypal/test', paypal_sample.process_payment),
    # path('accounts/password/reset/', django.contrib.auth.views.password_reset, {'password_reset_form': FrespoPasswordResetForm}, name='password_reset'),
    # path('accounts/register/', RegistrationView.as_view(form_class=MyRegForm), name='registration_register'),
    path('accounts/', include(registration.backends.default.urls)),   #for email activation
    # path('accounts/', include(registration.backends.simple.urls)),    #without email activation

    path('home/startIssue', main_views.homestartIssue),
    path('home/randomIssue', main_views.randomIssue),
    path('home/switchOldPage', main_views.switchOldPage),
    path('oldhome/', main_views.home, name='home'),
    path('rates', main_views.rates, name='rates'),
    path('404', TemplateView.as_view(template_name='404.html')),
    path('faq', TemplateView.as_view(template_name='issues/faq.html')),
    path('developers', TemplateView.as_view(template_name='issues/developers.html')),
    path('project/', include(core_urls.project_urls)),
    path('issuenew/', include(core_urls.issuenew_urls)),
    path('api/', include(core_urls.api_urls)),
    path('myissues/', issue_views.myissues),
    path('offer/', include(core_urls.offer_urls)),
    path('search/', issue_views.listIssues),   #should be without the slash
    path('tag/(?P<tag_slug>[-\w]+)/', issue_views.listIssues, name='issue-list-by-tag'),
    path('translate/', issue_views.listIssues),
    path('stats/',  main_views.stats),
    path('spa', TemplateView.as_view(template_name='spa.html')),
    path('jslic', TemplateView.as_view(template_name='issues/jslic.html')),
    path('github-hook/', include(core_urls.github_hook_urls)),
    path('feedback', include(core_urls.feedback_urls)),
    path('payment/', include(core_urls.payment_urls)),
    # path('github/', include(gh_frespo_integration.urls)),
    path('login-error/', main_views.login_error),
    path('robots.txt', TemplateView.as_view(template_name='issues/robots.txt', content_type='text/plain')),
    path('sitemap.xml', main_views.sitemap),
    path('email/', user_views.redirect_to_user_page, {'email_verified': 'true'}, name='emailmgr_email_list'),

    path('vuetest/', TemplateView.as_view(template_name='vuetest.html'))
    # path('email/activate/(?P<identifier>\w+)/', emailmgr.views.email_activate, name='emailmgr_email_activate'
]

# Add this only in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_ROOT_URL, document_root=settings.MEDIA_ROOT)