from apps.issues.models import Tag
from apps.issues.services import wikidata_services
from apps.issues.models import MultilingualTag, MultilingualTagTranslated, MultilingualTagIssue

__author__ = 'tony'


def addTag(name, objtype, objid):
    query = Tag.objects.filter(name=name, objtype=objtype, objid=objid)
    if query.count() == 0:
        tag = Tag(name=name, objtype=objtype, objid=objid)
        tag.save()
        return tag
    return None


def removeTag(name, objtype, objid):
    query = Tag.objects.filter(name=name, objtype=objtype, objid=objid)
    if query.count() == 0:
        return
    tag = query[0]
    tag.delete()


def addTagMultilingral(qid, title='', description=''):
    # get tag language
    # if tag exist return tag
    # if not exist, add tag and get all languages for tag

    found_tags = MultilingualTag.objects.filter(slug=qid)
    if found_tags.count() == 0:
        tag = MultilingualTag.create(qid, title, description)
        tag.save()
    # else:
        # tag = found_tags
    tag_info = wikidata_services.getConceptByQid(qid)
    tag_languages = []
    for item in tag_info:
        translated_tag = MultilingualTagTranslated.create(item['qid'], item['language'], item['content'], item['description'])
        tag_languages.append(translated_tag)

    MultilingualTagTranslated.deleteByQid(qid)
    MultilingualTagTranslated.objects.bulk_create(tag_languages)

    return tag


#add tags translations to database
def addTagMultilingralTranslations(qid):
    if MultilingualTagTranslated.objects.filter(qid=int(qid[1:])).count() > 0:
        return

    tag_info = wikidata_services.getConceptByQid(qid)
    tag_languages = []
    for item in tag_info:
        translated_tag = MultilingualTagTranslated.create(item['qid'], item['language'], item['content'], item['description'])
        tag_languages.append(translated_tag)
    MultilingualTagTranslated.objects.bulk_create(tag_languages)


def getIssueTagsForLanguage(issue_id, language):
    tag_issue_list = MultilingualTagIssue.objects.filter(issue_id=issue_id)
    qid_list = [item.qid for item in tag_issue_list]
    translated_list = MultilingualTagTranslated.objects.filter(qid__in=qid_list).filter(language=language)
    # if len(qid_list) != len(translated_list):
    #     raise Exception('MultilingualTagTranslated data does not match: issue_id:'+str(issue_id)+','+str(len(qid_list))+','+str(len(translated_list))+', language:'+language)

    item_list = {}
    for item in translated_list.values():
        item_list[item['qid']] = item

    result = []
    for item in tag_issue_list.values():
        if item['qid'] in item_list:
            item_language = item_list[item['qid']]
            result.append({
                'qid': 'q'+str(item_language['qid']),
                'title': item_language['content'],
                'description': item_language['description'],
            })
        else:
            result.append({
                'qid': 'q' + str(item['qid']),
                'title': item['title'],
                'description': item['description'],
            })
    return result


def getTagMuiltilingual(tag, language=None):
    return True