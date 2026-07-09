import requests
from apps.issues.models import MultilingualTagTranslated
import logging

__author__ = 'qingwei'

logger = logging.getLogger('issue')

def searchConcept(search, language='en', max_count=3):
    logger.info('start to search tags from server...')
    
    base_url = "https://www.wikidata.org/w/api.php"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }
    params = {
        "action": "wbsearchentities",
        "search": search,
        "language": language,
        "format": "json"
    }
    try:
        response = requests.get(base_url, params=params, headers=headers, timeout=10)
        response = response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Network request failed: {e}")
        return []
    except ValueError: # JSONDecodeError
        logger.error(f"Failed to decode JSON. Raw response was: {response.text}")
        return []

    result = []
    for item in response['search']:
        if len(result) == max_count:
            break
        qid = item['id']
        match_text = item['match']['text']
        description = item['description']
        #if language is not en, get the description from cencept info
        if language != 'en':
            for item_info in getConceptByQid(qid):
                if item_info['language'] == language and item_info['description']:
                    description = item_info['description']
                    break
        result.append({
            'qid': qid,
            'match_text': match_text,
            'label': item['label'],
            'description': description,
        })

    return result


def searchConceptFromLocal(search, language='en', max_count=3):
    print ('start to search tags from local:'+search+','+language)
    item_found = MultilingualTagTranslated.objects.filter(content__contains=search).filter(language=language)[:10]
    result = []
    for item in item_found.values():
        result.append({
            'qid': 'Q'+str(item['qid']),
            'match_text': item['content'],
            'label': item['content'],
            'description': item['description'],
        })

    return result


def getConceptByQid(qid):
    url = "https://www.wikidata.org/wiki/Special:EntityData/"+qid+".json"
    response = requests.get(url).json()
    info = response['entities'][qid]
    result = []

    for item in info['labels'].values():
        language = item['language']
        value = item['value']
        description = ''
        if language in info['descriptions']:
            description = info['descriptions'][language]['value']
        result.append({
            'qid': qid,
            'language': language,
            'content': value,
            'description': description,
        })
    return result
