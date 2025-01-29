import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from core.models import TechSolution, TechSolutionComment, Issue
from core.services import techSolution_services
from core.serializers import TechSolutionsSerializer, TechSolutionCommentSerializer
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view
from main_views import _throwIfNotObjAuthor
from core.utils.djangology_utils import djangology_quote, djangology_unquote

logger = logging.getLogger(__name__)

class TechSolutionDetail(APIView):
    # Get solution html template
    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request, solution_id=None, solution_name=None, format=None):
        if solution_id is not None:
            techSolution = get_object_or_404(TechSolution, pk=solution_id, deleted=False)
            return redirect('/solution/' +djangology_quote(techSolution.title), permanent=True)

        techSolution = get_object_or_404(TechSolution, title=djangology_unquote(solution_name), deleted=False)
        return Response({'solution': techSolution},
                        template_name='issues/solution.html')

    # Update a techSolution
    @method_decorator(login_required)
    def post(self, request, solution_id, format=None):
        techSolution = get_object_or_404(TechSolution, pk=solution_id)
        _throwIfNotObjAuthor(techSolution.createdByUser.id, request.user, "techSolution.id " + str(techSolution.id) )
        serializer = TechSolutionsSerializer(techSolution, data=request.data)
        if serializer.is_valid():
            techSolution = techSolution_services.edit_techSolution(techSolution, serializer, request.user)
            return redirect(techSolution.issue.get_view_link())
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete techSolution
    @method_decorator(login_required)
    def delete(self, request, solution_id, format=None):
        techSolution = get_object_or_404(TechSolution, pk=solution_id)
        _throwIfNotObjAuthor(techSolution.createdByUser.id, request.user, "techSolution.id " + str(techSolution.id) )
        techSolution_services.delete_techSolution(techSolution, request.user)
        return Response(TechSolutionsSerializer(techSolution).data, status=status.HTTP_200_OK)


class TechSolutionList(APIView):

    # Create new techSolution
    @method_decorator(login_required)
    def post(self, request, format=None):
        serializer = TechSolutionsSerializer(data=request.data)
        if serializer.is_valid():
            issue = get_object_or_404(Issue, pk=request.POST.get('issue'))
            techSolution_services.add_techSolution_to_issue(issue, serializer, request.user)
            return redirect(issue.get_view_link())

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TechSolutionCommentDetail(APIView):

    # Update a comment on techSolution
    @method_decorator(login_required)
    def post(self, request, pk, format=None):
        tComment = get_object_or_404(TechSolutionComment, pk=pk)
        _throwIfNotObjAuthor(tComment.author.id, request.user, "techSolution.id " + str(tComment.id))
        serializer = TechSolutionCommentSerializer(tComment, data=request.data)
        if serializer.is_valid():
            tComment = techSolution_services.edit_techSolutionComment(tComment, serializer, request.user)
            return redirect(tComment.techSolution.issue.get_view_link())
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TechSolutionCommentList(APIView):

    # Create new comment on techSolution
    @method_decorator(login_required)
    def post(self, request, tsolutionPk, format=None):
        serializer = TechSolutionCommentSerializer(data=request.data)
        if serializer.is_valid():
            techSolution = get_object_or_404(TechSolution, pk=tsolutionPk)
            techSolution_services.add_techSolutionComment(techSolution, serializer, request.user)
            return redirect(techSolution.issue.get_view_link())
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
