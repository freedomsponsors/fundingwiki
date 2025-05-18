import os

import numpy as np
import faiss
from django.db.models import When, Case
from openai import OpenAI, embeddings
import redis
import hashlib, time, random
import json

from apps.issues.models import Ideas
from apps.issues.services import faiss_services, redis_services, openai_services


# get suggest ideas for user
def get_user_suggest_ideas(user, number=10):
    user_embedding = faiss_services.get_user_embedding(user)

    indexes = faiss_services.query_faiss(user_embedding)
    ideas_list = get_ideas_by_faiss_ids(indexes, number, ideas_not_from_user=user)

    return ideas_list


# get suggest ideas for user cookie
def get_user_cookie_suggest_ideas(user_identify, number=10):
    if not user_identify:
        return []

    # get content list
    redis_key = 'site_ideas_' + user_identify
    idea_ids = redis_services.get_list(redis_key)
    ideas_content_list = Ideas.objects.filter(id__in=idea_ids).order_by('-date_created').values_list('content', flat=True)

    # get embedding
    embedding = faiss_services.get_embedding_from_text_list(ideas_content_list)

    # query faiss
    indexes = faiss_services.query_faiss(embedding)

    # get ideas
    ideas_list = get_ideas_by_faiss_ids(indexes, number, id_not_in=idea_ids)

    return ideas_list


# get suggest ideas for one specific idea
def get_suggest_by_idea(idea, number=10):
    embedding = faiss_services.get_embedding(idea.content)
    indexes = faiss_services.query_faiss(embedding)

    ideas_list = get_ideas_by_faiss_ids(indexes, number, id_not_in=[idea.id])

    return ideas_list


#get ideas by faiss ids
def get_ideas_by_faiss_ids(faiss_ids, number=10, id_not_in=None, ideas_not_from_user=False):
    ideas_list = Ideas.objects.filter(faiss_id__in=faiss_ids)

    if id_not_in:
        ideas_list = ideas_list.exclude(id__in=id_not_in)

    if ideas_not_from_user:
        ideas_list = ideas_list.exclude(createdByUser=ideas_not_from_user)

    # make the results in order of faiss_ids
    preserved = Case(*[When(faiss_id=pk, then=pos) for pos, pk in enumerate(faiss_ids)])
    ideas_list = ideas_list.order_by(preserved)[:number]

    return ideas_list


# generate one related ideas from one idea
def generate_one_related_ideas(idea_original):
    content = openai_services.generate_related_ideas(idea_original.content)

    # save idea
    idea = Ideas.newIdea(content=content)
    idea.idea_from = 'openai:' + str(idea_original.id)
    idea.faiss_id = faiss_services.add_to_faiss(idea.content)
    idea.save()





