# Create your views here.
from django.core.serializers import serialize
from django.http import JsonResponse
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from apps.issues.models import Ideas as IdeasModel
from apps.issues.serializers import IdeasSerializer
from rest_framework.response import Response

from apps.issues.services import faiss_services, idea_services, redis_services, openai_services


class Ideas(APIView):
    def get(self, request):
        ideas = IdeasModel.objects.order_by('-date_created').all()
        serializer = IdeasSerializer(ideas, many=True)

        return Response(serializer.data)

    def post(self, request):
        content = request.data.get('idea_content')
        idea = IdeasModel.newIdea(content=content)
        if request.user.is_authenticated:
            idea.createdByUser = request.user
            idea.idea_from = 'user'
        else:
            idea.idea_from = 'anonymous'

        idea.faiss_id = faiss_services.add_to_faiss(idea.content)
        idea.save()

        # update user embedding
        if request.user.is_authenticated:
            faiss_services.update_user_embedding(request.user)

        # if not authenticated, map to cookie id
        if not request.user.is_authenticated:
            user_identify = request.COOKIES.get('user_identify')
            if user_identify:
                redis_key = 'site_ideas_' + user_identify
                redis_services.add_to_list(redis_key, idea.id)
                print(redis_services.get_list(redis_key))

        #create a related idea
        idea_services.generate_one_related_ideas(idea)

        result = {
            'result': 'ok'
        }
        return JsonResponse(result)

    def delete(self, request):
        id = request.GET.get('id')
        item = get_object_or_404(IdeasModel, pk=id)
        item.delete()

        # update user embedding
        if request.user.is_authenticated:
            faiss_services.update_user_embedding(request.user)

        result = {
            'result': 'ok'
        }
        return JsonResponse(result)

class IdeasImport(APIView):
    def post(self, request):

        return Response({})


class IdeasMine(APIView):
    def get(self, request):
        ideas = []
        if request.user.is_authenticated:
            ideas = IdeasModel.objects.filter(createdByUser=request.user).order_by('-date_created').all()
        else:
            user_identify = request.COOKIES.get('user_identify')
            if user_identify:
                redis_key = 'site_ideas_' + user_identify
                idea_ids = redis_services.get_list(redis_key)
                ideas = IdeasModel.objects.filter(id__in=idea_ids).order_by('-date_created').all()

        serializer = IdeasSerializer(ideas, many=True)

        return Response(serializer.data)


class IdeasInterested(APIView):
    def get(self, request):
        idea_list = []
        if request.user.is_authenticated:
            idea_list = idea_services.get_user_suggest_ideas(request.user, number=5)
        else:
            user_identify = request.COOKIES.get('user_identify')
            idea_list = idea_services.get_user_cookie_suggest_ideas(user_identify, number=5)

        serializer = IdeasSerializer(idea_list, many=True)

        return Response(serializer.data)


class IdeasSimilar(APIView):
    def get(self, request):
        id = request.GET.get('id')
        print(id)
        idea = IdeasModel.objects.get(id=id)
        ideas_list = idea_services.get_suggest_by_idea(idea, 3)
        serializer = IdeasSerializer(ideas_list, many=True)

        return Response(serializer.data)


class User(APIView):
    def get(self, request):
        result = {
            'logged_in':0,
            'username':''
        }
        if request.user.is_authenticated:
            result['logged_in'] = 1
            result['username'] = request.user.username

        return Response(result)

















