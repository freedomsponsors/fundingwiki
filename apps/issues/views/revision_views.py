from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from apps.issues.models import TechSolutionHistEvent, TechSolution, Issue, IssueHistEvent
# from apps.issues.serializers import TechSolutionsHistEventSerializer, TechSolutionsSerializer, IssueSerializer
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from django.http import Http404
from rest_framework.response import Response
from apps.issues.services import revision_services
from apps.issues.utils.djangology_utils import djangology_quote, djangology_unquote
import json, urllib


def getCompareResponse(request, obj, serializeHistEventFunction, getStandardFunction, title):
    '''
    DRY class to process /compare response.
    :param request: original request with from and to parameters
    :param obj: object to get hist events (for example /solution/1/compare the obj is the tech solution with id=1)
    :param serializeHistEventFunction: function used to serialize a the revisioned object if is not the orifinal (pk=0)
    :param getStandardFunction: Function used to get the standard comparable object (see at revision_services.RevisionStandard)
    :param title: the title of the template
    :return: template rendered with al the parameters
    '''
    fromPk = request.GET.get('from')
    toPk = request.GET.get('to')
    if fromPk and toPk:
        from_ = obj if fromPk == '0' else serializeHistEventFunction(fromPk, obj)
        to = obj if toPk == '0' else serializeHistEventFunction(toPk, obj)

    from_ = getStandardFunction(from_)
    to = getStandardFunction(to)
    return Response({'title': title,
                     'object': obj,
                     'compare': from_.compare(to),
                     'from': from_, 'fromPk': fromPk,
                     'to': to, 'toPk': toPk, },
                    template_name='issues/history.html')


class IssueHistory(APIView):
    renderer_classes = (TemplateHTMLRenderer,)
    def get(self, request, issue_id, format=None):
        issue = get_object_or_404(Issue, pk=issue_id)
        return Response({'title': 'issue "'+issue.title+'"',
                         'object': issue},
                        template_name='issues/history.html')

class IssueCompare(APIView):

    def serializeIssueHistEvent(self, pk, issue):
        obj = get_object_or_404(IssueHistEvent, pk=pk, issue=issue)
        serialized = revision_services.serializeJson(obj.json, IssueSerializer, pk=pk)
        serialized.creationDate = obj.eventDate
        return serialized

    renderer_classes = (TemplateHTMLRenderer,)
    def get(self, request, issue_id, format=None):
        issue = get_object_or_404(Issue, pk=issue_id)
        return getCompareResponse(request, issue,
                                  self.serializeIssueHistEvent,
                                  revision_services.getIssueToStandard,
                                  'issue "' + issue.title + '"')


class TechSolutionHistory(APIView):
    renderer_classes = (TemplateHTMLRenderer,)
    def get(self, request, solution_id=None, solution_name=None, format=None):
        if solution_id is not None:
            solution = get_object_or_404(TechSolution, pk=solution_id, deleted=False)
            return redirect(
                '/solution/' + djangology_quote(solution.title) + "/history",
                permanent=True)

        techSolution = get_object_or_404(TechSolution, title=djangology_unquote(solution_name), deleted=False)
        return Response({'title': 'solution "'+techSolution.title+'"',
                         'object': techSolution},
                        template_name='issues/history.html')

class TechSolutionCompare(APIView):

    def serializeSolutionHistEvent(self, pk, techSolution):
        obj = get_object_or_404(TechSolutionHistEvent, pk=pk, techSolution=techSolution)
        serialized = revision_services.serializeJson(obj.json, TechSolutionsSerializer, pk=pk)
        serialized.creationDate = obj.eventDate
        return serialized

    renderer_classes = (TemplateHTMLRenderer,)
    def get(self, request, solution_id=None, solution_name=None, format=None):
        if solution_id is not None:
            solution = get_object_or_404(TechSolution, pk=solution_id, deleted=False)
            return redirect('/solution/' + djangology_quote(solution.title) + "/compare?" + urllib.urlencode(request.GET), permanent=True)

        solution = get_object_or_404(TechSolution, title=djangology_unquote(solution_name), deleted=False)
        return getCompareResponse(request, solution,
                                  self.serializeSolutionHistEvent,
                                  revision_services.getTechSolutionToStandard,
                                  'solution "' + solution.title + '"')