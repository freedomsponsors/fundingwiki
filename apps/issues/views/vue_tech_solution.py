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
from apps.issues.serializers import IssuesSerializer
from rest_framework.response import Response
from apps.issues.models import TechSolution as TechSolutionModel
from django.db.models import Q

from apps.issues.services import user_services

class TechSolution(APIView):
    def get(self, request):
        ideas = IssueModel.objects.order_by('-creationDate')

        # search by keyword
        search = request.GET.get('search', '')
        if search:
            ideas = ideas.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
        ideas = ideas.all()

        serializer = IssuesSerializer(ideas, many=True)

        return Response(serializer.data)

    def post(self, request):
        issue_id = request.data.get('issue_id')
        content = request.data.get('content')

        solution = TechSolutionModel()
        solution.title = ''
        solution.content = content
        solution.issue_id = issue_id

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
