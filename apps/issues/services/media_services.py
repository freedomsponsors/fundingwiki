from apps.issues.services.mail_services import notifyWatchers_newissuecomment
from apps.issues.models import ActionLog, MediaHistEvent, Watch, HistEventTypes, Media
from apps.issues.services import watch_services
from django.utils import timezone
from apps.issues.services.mail_services import notifyWatchers_newissuecomment

def delete_media(media, user):
    old_json = media.to_json()
    media.deleted = True
    media.save()
    event = MediaHistEvent.newChangeEvent(media, HistEventTypes.DELETE)
    event.save()
    ActionLog.log_delete_media(media=media, old_json=old_json, user=user)
    return media

def edit_media(media, serializer, user):
    old_json = media.to_json()
    event = MediaHistEvent.newChangeEvent(media, HistEventTypes.EDIT)
    serializer.save(updatedDate=timezone.now())
    ActionLog.log_edit_media(media=media, old_json=old_json)
    event.save()
    return media

def add_media_to_issue(issue, serializer, user, type, url, image):
    issue.touch()
    createdByUser = user
    creationDate = timezone.now()
    updatedDate = creationDate

    media = serializer.save(createdByUser=createdByUser,
                    issue=issue,
                    creationDate=creationDate,
                    updatedDate=updatedDate,
                    type=type,
                    url=url,
                    image=image)

    # If the user is not watching already the issue add it to the watch list
    watch_services.watch_issue(user, issue.id, Watch.ADDMEDIA)

    # watches = watch_services.find_issue_watches(issue)
    # notifyWatchers_newissuecomment(comment, watches)
    ActionLog.log_add_issue_media(media=media)
    return issue

def check_video_support(domain):
    return Media.isSupportedPlatform(domain)

