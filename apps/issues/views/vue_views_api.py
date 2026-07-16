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
from apps.issues.models import *
from django.db.models import Q, Count
from django.core.exceptions import ObjectDoesNotExist


from apps.issues.services import faiss_services, idea_services, redis_services, openai_services, user_services, wikidata_services


class Ideas(APIView):
    def get(self, request):
        ideas = IssueModel.objects.order_by('-creationDate')

        # search by keyword
        search = request.GET.get('search', '')
        if search:
            ideas = ideas.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
        
        ideas = ideas.annotate(solution_count=Count('techsolution'))

        serializer = IssuesSerializer(ideas, many=True)

        return Response(serializer.data)

    def post(self, request):
        content = request.data.get('idea_content')
        id = request.data.get('id')

        try:
            if id :
                idea = IssueModel.objects.get(id=id)

                content = content.strip()
                title_end = min(
                    (content.find('。') if content.find('。') != -1 else float('inf')),
                    (content.find('.') if content.find('.') != -1 else float('inf')),
                    (content.find('\n') if content.find('\n') != -1 else float('inf'))
                )
                if title_end != float('inf'):
                    idea.title = content[:title_end].strip()
                    content = content[title_end:].strip()
                else:
                    idea.title = content.strip()

                idea.description = content
            else:
                idea = IssueModel.newIssueSimple(content=content)
        except ObjectDoesNotExist:
            return Response({"code": 400, "msg": "record not exist:"+id}, status=400)

        if request.user.is_authenticated:
            idea.createdByUser = request.user
            idea.issue_from = 'user'
        else:
            idea.createdByUser = user_services.getAnonymousUser()
            idea.issue_from = 'anonymous'

        idea.faiss_id = faiss_services.add_to_faiss(idea.description)
        idea.save()

        # save tags
        tags = request.data.get('tags', [])
        if tags:    
            MultilingualTag.saveTags(tags, idea, bool(id))

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
        # idea_services.generate_one_related_ideas(idea)

        result = {
            'result': 'ok'
        }
        return JsonResponse(result)

    def delete(self, request):
        id = request.GET.get('id')
        item = get_object_or_404(IssueModel, pk=id)
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
            ideas = IssueModel.objects.filter(createdByUser=request.user).order_by('-creationDate').all()
        else:
            ideas = IssueModel.objects.none()
            user_identify = request.COOKIES.get('user_identify')
            if user_identify:
                redis_key = 'site_ideas_' + user_identify
                idea_ids = redis_services.get_list(redis_key)
                ideas = IssueModel.objects.filter(id__in=idea_ids).order_by('-creationDate').all()

        ideas = ideas.annotate(solution_count=Count('techsolution'))

        serializer = IssuesSerializer(ideas, many=True)

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

        serializer = IssuesSerializer(idea_list, many=True)

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
        idea = IssueModel.objects.get(id=id)
        ideas_list = idea_services.get_suggest_by_idea(idea, 3)
        serializer = IssuesSerializer(ideas_list, many=True)

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

    idea = IssueModel.objects.get(pk=idea_id)

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
    idea = IssueModel.objects.filter(id=id).annotate(solution_count=Count('techsolution')).first()
    
    serializer = IssuesSerializer(idea)
    serializer_data = serializer.data.copy()

    _add_vote_info_to_idea(request, serializer_data, [idea])

    serializer_data['count_solution'] = idea.techsolution_set.count()

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


@api_view(['GET'])
def get_languages(request):
    available_languages = Languages.available_languages();
    return Response(list(available_languages))


@api_view(['POST'])
def suggest_tags(request):
    search = request.data.get('search')
    language = request.data.get('language')
    if not language:
        language = request.user.getUserLanguage()

    result = wikidata_services.searchConcept(search, language, 3)
    print('suggest_tags result:', result)
    return Response(result)





