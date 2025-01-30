import logging
import traceback
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.cache import never_cache

from apps.issues.serializers import TechSolutionsSerializer
from apps.issues.templatetags.pagination import pagina
from django.contrib.auth.decorators import login_required
from django.contrib.syndication.views import Feed
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.template import RequestContext
from apps.issues.decorators import only_post
from apps.issues.models import *
from apps.issues.services import issue_services, watch_services, paypal_services, mail_services, techSolution_services
from apps.issues.views import paypal_views, bitcoin_views, HOME_CRUMB
# from frespo_currencies import currency_service


logger = logging.getLogger(__name__)

__author__ = 'tony'


@login_required
@only_post
def addSolution(request):
    serializer = TechSolutionsSerializer(data=request.POST)
    if serializer.is_valid():
        issue = get_object_or_404(Issue, pk=request.POST.get('issue'))
        techSolution_services.add_techSolution_to_issue(issue, serializer, request.user)
        return redirect(issue.get_view_link_new())
