# Create your views here.
from django.core.serializers import serialize
from django.http import JsonResponse
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from apps.issues.models import Ideas as IdeasModel
from apps.issues.serializers import IdeasSerializer
from rest_framework.response import Response

from apps.issues.services import faiss_services, idea_services, redis_services, openai_services, user_services


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
            idea.createdByUser = user_services.getAnonymousUser()
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
        if request.user.is_authenticated:
            ideas = IdeasModel.objects.filter(createdByUser=request.user).order_by('-date_created').all()
        else:
            user_identify = request.COOKIES.get('user_identify')
            if user_identify:
                redis_key = 'site_ideas_' + user_identify
                idea_ids = redis_services.get_list(redis_key)
                ideas = IdeasModel.objects.filter(id__in=idea_ids).order_by('-date_created').all()

        serializer = IdeasSerializer(ideas, many=True)

        # add voted info
        # check if voted
        # if request.user.is_authenticated:
        #     check_vote_user = request.user
        # else:
        #     check_vote_user = user_services.getAnonymousUser()
        # voted_idea_up_ids = idea_services.get_idea_ids_voted_up_by_user(check_vote_user, idea_list=ideas)
        # voted_idea_down_ids = idea_services.get_idea_ids_voted_down_by_user(check_vote_user, idea_list=ideas)
        for item in serializer.data:
            _add_vote_info_to_idea(request, item, ideas)
            # item['is_voted_up'] = item['id'] in voted_idea_up_ids
            # item['is_voted_down'] = item['id'] in voted_idea_down_ids

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

        # add voted info
        # check if voted
        # if request.user.is_authenticated:
        #     check_vote_user = request.user
        # else:
        #     check_vote_user = user_services.getAnonymousUser()
        # voted_idea_up_ids = idea_services.get_idea_ids_voted_up_by_user(check_vote_user, idea_list=idea_list)
        # voted_idea_down_ids = idea_services.get_idea_ids_voted_down_by_user(check_vote_user, idea_list=idea_list)
        for item in serializer.data:
            _add_vote_info_to_idea(request, item, idea_list)
            # item['is_voted_up'] = item['id'] in voted_idea_up_ids
            # item['is_voted_down'] = item['id'] in voted_idea_down_ids

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


@api_view(['POST'])
def idea_vote(request):
    idea_id = request.data.get('id')
    vote_type = request.data.get('vote_type')

    idea = IdeasModel.objects.get(pk=idea_id)

    if request.user.is_authenticated:
        user = request.user
    else:
        user = user_services.getAnonymousUser()

    if vote_type == 'up':
        idea_services.vote_idea_up(idea, user)
    elif vote_type == 'up_cancel':
        idea_services.vote_idea_up_cancel(idea, user)
    elif vote_type == 'up_from_down':
        idea_services.vote_idea_down_cancel(idea, user)
        idea_services.vote_idea_up(idea, user)
    elif vote_type == 'down':
        idea_services.vote_idea_down(idea, user)
    elif vote_type == 'down_cancel':
        idea_services.vote_idea_down_cancel(idea, user)
    elif vote_type == 'down_from_up':
        idea_services.vote_idea_up_cancel(idea, user)
        idea_services.vote_idea_down(idea, user)

    result = {
        'result': 'success'
    }

    return Response(result)


@api_view(['GET'])
def get_idea_by_id(request):
    id = request.query_params.get('id')
    idea = IdeasModel.objects.get(id=id)
    serializer = IdeasSerializer(idea)
    serializer_data = serializer.data.copy()

    _add_vote_info_to_idea(request, serializer_data, [idea])

    return Response(serializer_data)


def _add_vote_info_to_idea(request, data, idea_list):
    if request.user.is_authenticated:
        check_vote_user = request.user
    else:
        check_vote_user = user_services.getAnonymousUser()

    voted_idea_up_ids = idea_services.get_idea_ids_voted_up_by_user(check_vote_user, idea_list=idea_list)
    voted_idea_down_ids = idea_services.get_idea_ids_voted_down_by_user(check_vote_user, idea_list=idea_list)

    data['is_voted_up'] = data['id'] in voted_idea_up_ids
    data['is_voted_down'] = data['id'] in voted_idea_down_ids

    vote_ope = idea_services.get_ope_by_up_down_status(data['is_voted_up'], data['is_voted_down'])
    data['vote_up_ope'] = vote_ope['vote_up_ope']
    data['vote_down_ope'] = vote_ope['vote_down_ope']











