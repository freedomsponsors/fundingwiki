import logging
import requests
from django.utils.translation import gettext as _
from apps.issues.models import *
import xxhash
import redis
from django.conf import settings

logger = logging.getLogger(__name__)

redis_client = redis.StrictRedis(host=settings.REDIS['host'], port=settings.REDIS['port'], db=settings.REDIS['db'], password=settings.REDIS['pass'], decode_responses=True)

def get_language_name_from_code(code):
    if not code:
        return ''

    key = 'language_name_' + code
    language_name = redis_client.get(key)
    if language_name:
        logger.info('get language from redis')
        return language_name

    logger.info('search for the language code:'+code)
    language = Languages.objects.get(code=code)
    redis_client.set(key, language.name)
    logger.info('get language from database')
    return language.name


def update_language_if_empty(issue):
    if not issue.language:
        issue.language = detect_language(issue.title)
        issue.save()


def get_language_list():
    language_list = Languages.objects.all()

    result = []
    for item in language_list:
        result.append({
            'code': item.code,
            'label': _(item.name)
        })
    return result


def get_language_list_from_server():
    url = "http://192.243.108.188:5000/languages"
    response = requests.get(url).json()
    result = []
    for item in response:
        result.append({
            'code': item['code'],
            'label': item['name']
        })
    return result


def detect_language(text):
    logger.info('detect from server')

    url = "http://192.243.108.188:5000/detect"
    response = requests.post(url, json={"q": text}).json()
    return response[0]['language']


def translate_text(text, target_language, source_language=None):
    result = {
        'if_success': 0,
        'result': '',
        'source_language': '',
        'target_language': target_language
    }
    text = text.encode('utf-8')
    hash = xxhash.xxh3_64(text).hexdigest()

    # check the database first
    item = ContentTranslated.objects.filter(hash=hash, target_language=target_language).first()
    if item:
        result['if_success'] = 1
        result['result'] = item.content_translated
        result['source_language'] = item.source_language
        logger.info('translation found in database')
        return result

    # if not found in the database, get the translation from server
    info = translate_text_from_server(text, target_language, source_language)
    if info['if_success']:
        obj_translate = ContentTranslated.newContentTranslated(hash=hash, source_language=info['source_language'], target_language=target_language, content_translated=info['result'])
        obj_translate.save()

    result['if_success'] = info['if_success']
    result['result'] = info['result']
    result['source_language'] = info['source_language']
    return result


def translate_text_from_server(text, target_language, source_language=None):
    logger.info('request the translate from server')
    result = {
        'if_success': 0,
        'result': '',
        'source_language': source_language,
        'target_language': target_language
    }
    try:
        if not source_language:
            source_language = detect_language(text)
            result['source_language'] = source_language

        if target_language != source_language:
            url = "http://192.243.108.188:5000/translate"
            response = requests.post(url, json={
                "q": text,
                "source": source_language,
                "target": target_language,
                "format": 'html'
            }).json()
            result['result'] = response["translatedText"]
        else:
            result['result'] = text

        result['if_success'] = 1
    except:
        result['result'] = 'translate failed...'

    return result
