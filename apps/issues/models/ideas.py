from django.contrib.auth.models import User, AnonymousUser
from django.contrib.gis.db import models
from django.utils import timezone

class Ideas(models.Model):
    content = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(null=False)
    point = models.IntegerField(default=0)
    faiss_id = models.IntegerField(default=-1, db_index=True)
    createdByUser = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    idea_from = models.CharField(max_length=256, null=True, blank=True)

    @classmethod
    def newIdea(cls, content):
        idea = cls()
        idea.content = content
        idea.date_created = timezone.now()
        return idea


    def add_point(self, point=1):
        self.point += point
        self.save()

    def __str__(self):
        return self.content

    def if_voted_up(self, user):
        return UserIdeaVote.objects.filter(idea=self, user=user, voteType='UP').count() > 0

    def if_voted_down(self, user):
        return UserIdeaVote.objects.filter(idea=self, user=user, voteType='DOWN').count() > 0


class UserIdeaVote(models.Model):
    idea = models.ForeignKey(Ideas, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    voteCreated = models.DateTimeField()
    voteType = models.CharField(max_length=20)

    @classmethod
    def newVoteUp(cls, user, idea):
        vote = cls()
        vote.user = user
        vote.idea = idea
        vote.voteType = 'UP'
        vote.voteCreated = timezone.now()
        return vote

    @classmethod
    def newVoteDown(cls, user, idea):
        vote = cls()
        vote.user = user
        vote.idea = idea
        vote.voteType = 'DOWN'
        vote.voteCreated = timezone.now()
        return vote

    def saveVote(self):
        if UserIdeaVote.objects.filter(idea=self.idea, user=self.user, voteType=self.voteType).count() == 0:
            self.save()

    def cancelVote(self):
        UserIdeaVote.objects.filter(idea=self.idea, user=self.user, voteType=self.voteType).delete()



