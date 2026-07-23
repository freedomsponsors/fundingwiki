# Create your views here.
from django.core.serializers import serialize
from django.http import JsonResponse
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from apps.issues.models import Issue as IssueModel
from apps.issues.serializers import TechSolutionsSerializer, TechSolutionCommentSerializer
from rest_framework.response import Response
from apps.issues.models import TechSolution as TechSolutionModel, TechSolutionComment as TechSolutionCommentModel
from django.db.models import Q

from apps.issues.services import user_services

class TechSolution(APIView):
    def get(self, request):
        issue_id = request.GET.get('issue_id')
        solutions = TechSolutionModel.objects.filter(issue_id=issue_id).order_by('id')

        solutions = solutions.prefetch_related("techsolutioncomment_set")
        solutions = solutions.prefetch_related("techsolutioncomment_set__author").all()

        serializer = TechSolutionsSerializer(solutions, many=True, context={"request": request})

        return Response(serializer.data)

    def post(self, request):
        issue_id = request.data.get('issue_id')
        content = request.data.get('content')
        solution_id = request.data.get('id')

        if solution_id:
            try:
                solution = TechSolutionModel.objects.get(id=solution_id)
            except TechSolutionModel.DoesNotExist:
                return JsonResponse({"result": "error", "msg": "solution not exist"}, status=404)
        else:
            solution = TechSolutionModel()
            solution.title = ''

        solution.content = content
        solution.issue_id = issue_id

        if not solution_id:
            if request.user.is_authenticated:
                solution.createdByUser = request.user
            else:
                solution.createdByUser = user_services.getAnonymousUser()

        solution.save()

        result = {
            'result': 'ok'
        }
        return JsonResponse(result)

    def delete(self, request):
        result = {
            'result': 'ok'
        }
        return JsonResponse(result)


class TechSolutionComment(APIView):
    def get(self, request):
        return Response({})

    def post(self, request):
        solution_id = request.data.get('solution_id')
        content = request.data.get('content')

        solutionComment = TechSolutionCommentModel()
        solutionComment.content = content
        solutionComment.techSolution_id = solution_id

        if request.user.is_authenticated:
            solutionComment.author = request.user
        else:
            solutionComment.author = user_services.getAnonymousUser()

        solutionComment.save()

        result = {
            'result': 'ok'
        }
        return JsonResponse(result)

    def delete(self, request):
        return JsonResponse({})
