from core.services.mail_services import notifyWatchers_newissuecomment
from core.models import ActionLog, TechSolutionHistEvent, Watch, HistEventTypes, TechSolutionCommentHistEvent
from core.services import watch_services
from django.utils import timezone

def delete_techSolution(techSolution, user):
    old_json = techSolution.to_json()
    techSolution.deleted = True
    techSolution.save()
    event = TechSolutionHistEvent.newChangeEvent(techSolution, HistEventTypes.DELETE)
    event.save()
    ActionLog.log_delete_techSolution(techSolution=techSolution, old_json=old_json, user=user)
    return techSolution


def edit_techSolution(techSolution, serializer, user):
    old_json = techSolution.to_json()
    event = TechSolutionHistEvent.newChangeEvent(techSolution, HistEventTypes.EDIT)
    serializer.save(updatedDate=timezone.now())
    ActionLog.log_edit_techSolution(techSolution=techSolution, old_json=old_json)
    event.save()
    return techSolution

def add_techSolution_to_issue(issue, serializer, user):
    issue.touch()
    createdByUser = user
    creationDate = timezone.now()
    updatedDate = creationDate

    techSolution = serializer.save(createdByUser=createdByUser,
                    issue=issue,
                    creationDate=creationDate,
                    updatedDate=updatedDate)

    # If the user is not watching already the issue add it to the watch list
    watch_services.watch_issue(user, issue.id, Watch.ADDTECHSOLUTION)

    # watches = watch_services.find_issue_watches(issue)
    # notifyWatchers_newissuecomment(comment, watches)
    ActionLog.log_add_issue_techSolution(techSolution=techSolution)
    return issue


def edit_techSolutionComment(tComment, serializer, user):
    old_json = tComment.to_json()
    event = TechSolutionCommentHistEvent.newChangeEvent(tComment, HistEventTypes.EDIT)
    serializer.save()
    ActionLog.log_edit_techSolution_comment(tComment=tComment, old_json=old_json)
    event.save()
    return tComment

def add_techSolutionComment(techSolution, serializer, user):
    author = user
    creationDate = timezone.now()

    tComment = serializer.save(author=author,
                                   techSolution=techSolution,
                                   creationDate=creationDate,)

    watch_services.watch_issue(user, techSolution.issue.id, Watch.ADDTECHSOLUTIONCOMMENT)

    # watches = watch_services.find_issue_watches(issue)
    # notifyWatchers_newissuecomment(comment, watches)
    ActionLog.log_add_techSolution_comment(techSolution=techSolution, tComment=tComment)
    return tComment