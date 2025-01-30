import json
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.issues.templatetags.pagination import pagina
from django.shortcuts import render, redirect
from apps.issues.decorators import only_post
from apps.issues.models import Project, ActionLog, Languages
from apps.issues.services import stats_services, issue_services, watch_services, mail_services
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from apps.issues.utils.djangology_utils import djangology_quote, djangology_unquote
from django.views.decorators.cache import never_cache
import logging


__author__ = 'tony'

@never_cache
def view(request, project_id=None, project_name=None):
    if project_id is not None:
        project = get_object_or_404(Project, pk=project_id)
        return redirect('/project/' + djangology_quote(project.name), permanent=True)

    project = get_object_or_404(Project, name=djangology_unquote(project_name))
    if project.redirectto_project:
        do_redirect = 'false' != request.GET.get('redirect')
        if do_redirect:
            return redirect(project.redirectto_project.get_view_link())
    # logging.info(project.id)
    # logging.info('id:' + str(project_id))
    project_id = project.id

    stats = stats_services.project_stats(project)
    issues_sponsoring = issue_services.search_issues(project_id=project_id, is_sponsored=True)[0:3]
    issues_kickstarting = issue_services.search_issues(project_id=project_id, is_sponsored=False)[0:3]
    issues_sponsoring = json.dumps(issue_services.to_card_dict(issues_sponsoring))
    issues_kickstarting = json.dumps(issue_services.to_card_dict(issues_kickstarting))
    top_sponsors = stats_services.project_top_sponsors(project_id)[0:5]
    top_programmers = stats_services.project_top_programmers(project_id)[0:5]
    is_watching = request.user.is_authenticated() and watch_services.is_watching_project(request.user, project.id)
    return render(request, 'issues/project.html',
                              {'project': project,
                               'stats': stats,
                               'tags': json.dumps([t.name for t in project.get_tags()]),
                               'issues_sponsoring': issues_sponsoring,
                               'issues_kickstarting': issues_kickstarting,
                               'top_sponsors': top_sponsors,
                               'top_programmers': top_programmers,
                               'is_watching': is_watching,
                               })


@login_required
@never_cache
def edit_form(request, project_id=None, project_name=None):
    if project_id is not None:
        project = get_object_or_404(Project, pk=project_id)
        return redirect('/project/' + djangology_quote(project.name) + '/edit', permanent=True)

    project = get_object_or_404(Project, name=djangology_unquote(project_name))

    # avalible languages
    available_languages = Languages.available_languages();

    return render(request, 'issues/project_edit.html', {'project': project, 'available_languages':available_languages})


@login_required
@only_post
def edit(request):
    project_id = int(request.POST.get('id'))
    project = Project.objects.get(pk=project_id)
    old_json = project.to_json()
    if 'image3x1' in request.FILES and request.FILES['image3x1']:
        project.image3x1 = request.FILES['image3x1']
    project.description = request.POST.get('description')
    project.homeURL = request.POST.get('homeURL')
    project.language = request.POST.get('language')
    project.save()
    watches = watch_services.find_project_watches(project)
    mail_services.notifyWatchers_project_edited(request.user, project, old_json, watches)
    ActionLog.log_edit_project(project=project, user=request.user, old_json=old_json)
    return redirect('/project/%s' % project.id)


def list(request):
    proj_list = Project.objects.all().order_by('name')
    projects = pagina(request, proj_list)
    return render(request, 'issues/project_list.html', {'projects':projects})
