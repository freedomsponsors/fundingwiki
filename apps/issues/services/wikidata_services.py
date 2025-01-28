import requests
from apps.issues.models import MultilingualTagTranslated
__author__ = 'qingwei'


def searchConcept(search, language='en', max_count=3):
    print('start to search tags from server...')
    url = "https://www.wikidata.org/w/api.php?action=wbsearchentities&search="+search+"&language="+language+"&format=json"
    response = requests.get(url).json()
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
    # print result
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

    for item in info['labels'].itervalues():
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
