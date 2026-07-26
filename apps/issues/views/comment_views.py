from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _
from django.template import RequestContext
from apps.issues.decorators import only_post
from apps.issues.models import *
from apps.issues.services import comment_services, watch_services
from apps.mediawiki_auth.decorators import requires_identity

__author__ = 'tony'

@requires_identity(level='guest', api_only=False)
@only_post
def addIssueComment(request):
    issue_id = int(request.POST['issue_id'])
    comment_content = request.POST['content']

    mw_user = getattr(request, 'mw_user', None)
    if mw_user:
        author = mw_user
        # watch_services.watch_issue(mw_user, issue_id, Watch.COMMENTED)
    else:
        author = user_services.getAnonymousUser()

    issue = comment_services.add_comment_to_issue(issue_id, comment_content, author)
    return redirect(issue.get_view_link())


@login_required
@only_post
def editIssueComment(request):
    comment_id = int(request.POST['comment_id'])
    comment_content = request.POST['content']
    comment = comment_services.edit_comment_of_issue(comment_id, comment_content, request.user)
    return redirect(comment.issue.get_view_link())


def viewIssueCommentHistory(request, comment_id):
    comment = IssueComment.objects.get(pk = comment_id)
    comment_events = IssueCommentHistEvent.objects.filter(comment__id = comment_id).order_by("eventDate")
    return render(request, 'issues/comment_history.html',
        {'comment':comment,
         'comment_events':comment_events,})
