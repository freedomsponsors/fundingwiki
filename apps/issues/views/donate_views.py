from django.shortcuts import redirect, render, get_object_or_404
from apps.issues.models import *

logger = logging.getLogger(__name__)

def donate(request):
    return render(request, 'issues/donate.html', {})