import os

import numpy as np
import faiss
from openai import OpenAI
import redis
import hashlib, time, random
import json
from langdetect import detect

from apps.issues.models import Ideas
from apps.issues.services import redis_services

# client for openai
client = OpenAI(api_key='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')

# generate related ideas, for one idea about cost total_tokens=127
def generate_related_ideas(user_idea, number=1):
    print('call openai to generate related ideas', user_idea)

    # prompt = (
    #     f"Generate {number} creative and unique ideas based on the following concept:\n\n"
    #     f"'{user_idea}'\n\n"
    #     f"Each idea should be a separate paragraph and around 20 to 30 words long."
    # )

    language = detect(user_idea)
    print('original language:', language)

    prompt = {
        'en': f"Give me a creative new idea similar to: {user_idea}",
        'es': f"Dame una nueva idea creativa similar a: {user_idea}",
        'zh-cn': f"给我一个与这个类似的创意想法：{user_idea}",
        # Add more languages if needed
    }.get(language, f"Give me a creative new idea similar to: {user_idea}")

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  #gpt-4
        messages=[
            {"role": "system", "content": "You are a creative idea generator."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8,
        max_tokens=500,  # increased to allow more words
    )
    ideas = response.choices[0].message.content
    return ideas


# Function to get embeddings for a piece of text
def get_embedding(text):
    key = 'embedding_' + hashlib.md5(text.encode('utf-8')).hexdigest()

    #try to get from redis
    cached_embedding = redis_services.get(key)
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
        redis_services.set(key, json.dumps(embedding))
        return embedding
    except Exception as e:
        print(e)
        return None
