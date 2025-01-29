from django.urls import path
from apps.issues.views import issue_views
from apps.issues.views import comment_views
from apps.issues.views import media_views
from apps.issues.views import revision_views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('rss', issue_views.listIssuesFeed),
    path('sponsor/submit', issue_views.sponsorIssue),
    path('sponsor', issue_views.addIssueForm),
    path('add/submit', issue_views.addIssue),
    path('kickstart/submit', issue_views.kickstartIssue),
    path('add/', issue_views.addIssueForm),
    path('edit/submit', issue_views.editIssue),
    path('saveProjectName', issue_views.saveProjectName),
    # Djangology urls
    path('(?P<issue_id>\d+)/history', revision_views.IssueHistory.as_view()),
    path('(?P<issue_id>\d+)/compare', revision_views.IssueCompare.as_view()),
    # End djangology urls
    path('(?P<issue_id>\d+)/', issue_views.viewIssue),
    path('(?P<issue_id>\d+)/.*', issue_views.viewIssue),
    path('new/(?P<issue_id>\d+)/.*', issue_views.viewIssueNew),
    path('vote', issue_views.vote),
    path('vote_solution', issue_views.voteSolution),
]

urlpatterns += [
    path('comment/add/submit', comment_views.addIssueComment),
    path('comment/edit/submit', comment_views.editIssueComment),
    path('comment/(?P<comment_id>\d+)/history', comment_views.viewIssueCommentHistory),
]

# Filter issues by tag
urlpatterns += [
    path('tag/(?P<tag_slug>[-\w]+)/', issue_views.listIssues, name='issues_by_tag'),
]

# Djangology urls
urlpatterns += [
    path('media/([0-9]+)', media_views.MediaDetail.as_view()),
    path('media/', media_views.MediaList.as_view()),
]
#