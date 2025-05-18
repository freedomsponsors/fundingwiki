from django.contrib.auth.models import User, AnonymousUser
from django.contrib.gis.db import models
from django.utils import timezone

class Ideas(models.Model):
    content = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(null=False)
    reputation = models.IntegerField(default=0)
    faiss_id = models.IntegerField(default=-1, db_index=True)
    createdByUser = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    idea_from = models.CharField(max_length=256, null=True, blank=True)

    @classmethod
    def newIdea(cls, content):
        idea = cls()
        idea.content = content
        idea.date_created = timezone.now()
        return idea

    def __str__(self):
        return self.content