import os

import numpy as np
import faiss
from openai import OpenAI
import redis
import hashlib, time, random
import json
from django.conf import settings

from apps.issues.models import Ideas

# redis client
redis_client = redis.StrictRedis(host=settings.REDIS['host'], port=settings.REDIS['port'], db=settings.REDIS['db'], password=settings.REDIS['pass'], decode_responses=True)

# get user embedding
def set(key, value):
    redis_client.set(key, value)


def get(key):
    return redis_client.get(key)


def delete(key):
    redis_client.delete(key)


def add_to_list(key, value):
    print('add to list: ', key, value)
    redis_client.lpush(key, value)


def get_list(key, start=0, end=-1):
    print('get list: ', key, start, end)
    return redis_client.lrange(key, start, end)
