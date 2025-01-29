from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from apps.issues.models import *
from apps.issues.services import media_services
# from apps.issues.serializers import MediaSerializer
from rest_framework.views import APIView
from django.http import Http404
from django.core.validators import URLValidator, ValidationError
# from urlparse import urlparse
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
# from main_views import _throwIfNotObjAuthor
from rest_framework.decorators import api_view


class MediaDetail(APIView):

    def get_object(self, pk):
        try:
            return Media.objects.get(pk=pk)
        except Media.DoesNotExist:
            raise Http404

    # Update a media
    # TODO: Set values that you can modify only title and content never url or type
    @method_decorator(login_required)
    def post(self, request, pk, format=None):
        media = self.get_object(pk)
        _throwIfNotObjAuthor(media.createdByUser.id, request.user, "media.id " + str(media.id) )
        serializer = MediaSerializer(media, data=request.data)
        if serializer.is_valid():
            media = media_services.edit_media(media, serializer, request.user)
            return redirect(media.issue.get_view_link())
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete media
    @method_decorator(login_required)
    def delete(self, request, pk, format=None):
        media = get_object_or_404(Media, pk=pk)
        _throwIfNotObjAuthor(media.createdByUser.id, request.user, "media.id " + str(media.id) )
        media_services.delete_media(media, request.user)
        return Response(MediaSerializer(media).data, status=status.HTTP_200_OK)

class MediaList(APIView):

    # Create new media
    @method_decorator(login_required)
    def post(self, request, format=None):
        serializer = MediaSerializer(data=request.data)
        if serializer.is_valid():
            type = request.POST.get('type')
            issue = get_object_or_404(Issue, pk=request.POST.get('issue'))

            url = request.POST.get('url')
            img = ''
            if (type == "video" or type == "url"):
                val = URLValidator()
                val(url)
                if type == "video" and not media_services.check_video_support('{uri.netloc}'.format(uri=urlparse(url))):
                    raise ValidationError("Not supported video platform")

            elif type == "image":
                if 'image' in request.FILES and request.FILES['image']:
                    img = request.FILES['image']

            media_services.add_media_to_issue(issue, serializer, request.user, type=type, url=url, image=img)
            return redirect(issue.get_view_link())
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)