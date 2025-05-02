from django.urls import path
from apps.issues.views import issue_views, revision_views, techSolution_views


urlpatterns = [
    path('add/submit', issue_views.addSolution),
    path('abort/submit', issue_views.abortSolution),
    path('resolve/submit', issue_views.resolveSolution),
]

# Djangology urls
urlpatterns += [
    path('(?P<solution_id>\d+)/history', revision_views.TechSolutionHistory.as_view()),
    path('(?P<solution_id>\d+)/compare', revision_views.TechSolutionCompare.as_view()),
    path('(?P<solution_name>.+)/history', revision_views.TechSolutionHistory.as_view()),
    path('(?P<solution_name>.+)/compare', revision_views.TechSolutionCompare.as_view()),
]

urlpatterns += [
    path('([0-9]+)/comment/', techSolution_views.TechSolutionCommentList.as_view()),
    path('(?P<solution_id>\d+)', techSolution_views.TechSolutionDetail.as_view()),
    path('(?P<solution_name>.+)', techSolution_views.TechSolutionDetail.as_view()),
    path('comment/([0-9]+)', techSolution_views.TechSolutionCommentDetail.as_view()),
    path('', techSolution_views.TechSolutionList.as_view()),
]
