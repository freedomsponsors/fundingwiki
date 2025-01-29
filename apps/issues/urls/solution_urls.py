from django.conf.urls import url
from core.views import issue_views, revision_views, techSolution_views


urlpatterns = [
    url(r'^add/submit$', issue_views.addSolution),
    url(r'^abort/submit$', issue_views.abortSolution),
    url(r'^resolve/submit$', issue_views.resolveSolution),
]

# Djangology urls
urlpatterns += [
    url(r'^(?P<solution_id>\d+)/history', revision_views.TechSolutionHistory.as_view()),
    url(r'^(?P<solution_id>\d+)/compare', revision_views.TechSolutionCompare.as_view()),
    url(r'^(?P<solution_name>.+)/history', revision_views.TechSolutionHistory.as_view()),
    url(r'^(?P<solution_name>.+)/compare', revision_views.TechSolutionCompare.as_view()),
]

urlpatterns += [
    url(r'^([0-9]+)/comment', techSolution_views.TechSolutionCommentList.as_view()),
    url(r'^(?P<solution_id>\d+)', techSolution_views.TechSolutionDetail.as_view()),
    url(r'^(?P<solution_name>.+)', techSolution_views.TechSolutionDetail.as_view()),
    url(r'^comment/([0-9]+)', techSolution_views.TechSolutionCommentDetail.as_view()),
    url(r'^', techSolution_views.TechSolutionList.as_view()),
]
