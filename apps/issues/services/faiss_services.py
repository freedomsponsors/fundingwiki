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

# client for openai
client = OpenAI(api_key='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')

# Initialize Faiss index
dimension = 1536  # For the model we are using (e.g., text-embedding-ada-002)

# init faiss index
FAISS_INDEX_PATH = "faiss_index.index"
if os.path.exists(FAISS_INDEX_PATH):
    index = faiss.read_index(FAISS_INDEX_PATH)
else:
    index = faiss.IndexFlatL2(dimension)


# Function to query the FAISS index by a specific embedding
def query_faiss(embedding):
    number = 100
    embedding = np.array([embedding]).astype('float32')

    # Search for similar ideas
    try:
        distances, indexes = index.search(embedding, number)
        return indexes[0]
    except Exception as e:
        print(e)
        return []


# Function to add a piece of text to the FAISS index
def add_to_faiss(text):
    embedding = get_embedding(text)  # Get the embedding for the idea
    print('embedding from text:', embedding)
    embedding = np.array([embedding]).astype('float32')
    print('embedding:', embedding)
    # Add embeddings to the FAISS index
    try:
        index.add(embedding)
    except Exception as e:
        print(e)
        return -1

    print("Number of vectors in the index:", index.ntotal)

    faiss_id = index.ntotal - 1

    print('faiss_id:', faiss_id)

    faiss.write_index(index, FAISS_INDEX_PATH)

    return faiss_id


# get user embedding
def get_user_embedding(user, force_update=False):
    key = 'embedding_user_' + str(user.id)

    cached_embedding = redis_client.get(key)
    if cached_embedding and not force_update:
        print('get user embedding from redis')
        return json.loads(cached_embedding)

    # get all the ideas created by the user
    ideas = Ideas.objects.filter(createdByUser=user).all()

    # create a list of embeddings
    embedding_user = []
    for idea in ideas:
        embedding_user.append(get_embedding(idea.content))
    embedding_user = np.mean(embedding_user, axis=0)

    redis_client.set(key, json.dumps(embedding_user.tolist()))
    return embedding_user


# update user embedding
def update_user_embedding(user):
    get_user_embedding(user, True)


def get_embedding_from_text_list(text_list):
    embedding_list = []
    for text in text_list:
        embedding_list.append(get_embedding(text))

    return np.mean(embedding_list, axis=0)


# Function to get embeddings for a piece of text
def get_embedding(text):
    key = 'embedding_' + hashlib.md5(text.encode('utf-8')).hexdigest()

    #try to get from redis
    cached_embedding = redis_client.get(key)
    if cached_embedding:
        print('get embedding from redis')
        embedding = json.loads(cached_embedding)
        return embedding

    try:
        print('=============get embedding from openai=====================')
        embedding = client.embeddings.create(
            model="text-embedding-3-small",  # OpenAI model for embeddings
            input=text
        ).data[0].embedding
        redis_client.set(key, json.dumps(embedding))
        print('get embedding from openai, result: ', embedding)
        return embedding
    except Exception as e:
        print(e)
        return None
