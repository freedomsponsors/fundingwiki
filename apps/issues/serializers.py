from rest_framework import serializers
from apps.issues.models import *
from django.conf import settings
from apps.issues.utils.djangology_utils import djangology_url_special_chars

# This file contains serializers used by Djangology project

class MediaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Media
        fields = ('id', 'title', 'content', 'url', 'createdByUser', 'karma', 'type', 'issue', 'creationDate', 'updatedDate', 'deleted', 'image')
        read_only_fields = ('id', 'createdByUser', 'karma', 'creationDate', 'issue', 'deleted', 'type', 'updatedDate', 'url', 'image')

    def create(self, validated_data):
        return Media.objects.create(**validated_data)


class TechSolutionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechSolution
        fields = ('id', 'title', 'content', 'createdByUser', 'karma', 'issue', 'creationDate', 'updatedDate', 'deleted')
        read_only_fields = ('id', 'createdByUser', 'karma', 'creationDate', 'issue', 'deleted')

    def validate_title(self, value):
        if djangology_url_special_chars(value):
            raise serializers.ValidationError("Name characters not allowed")
        return value

    # Create an object without save it on db
    def generate(self):
        return TechSolution(**self.validated_data)

class TechSolutionCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechSolutionComment
        fields = ('id', 'author', 'creationDate', 'content')
        read_only_fields = ('id', 'author', 'creationDate')

class TechSolutionsHistEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechSolutionHistEvent
        fields = ('id', 'eventDate', 'json', 'event', 'techSolution')


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ('id', 'title', 'description', 'creationDate', 'updatedDate', 'createdByUser')
        read_only_fields = ('id', 'createdByUser', 'creationDate')
    # Create an object without save it on db
    def create(self):
        return Issue(**self.validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class IdeasSerializer(serializers.ModelSerializer):
    createdByUser = UserSerializer()
    class Meta:
        model = Ideas
        fields = '__all__'
