from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .utils import find_average
from . import serializers, models

class ComicViewSet(ModelViewSet):
    serializer_class = serializers.ComicSerializer
    queryset = models.Comic.objects.select_related("author").all()

class CreateRating(APIView):
    def post(self, request, format=None):
        ser = serializers.RatingSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        try:    
            rated = models.Rating.objects.get(comic_id=request.data['comic_id'], user_id=request.data['user_id'])
            if rated.user_id.pk != request.data['user_id']:
                ser.save()
            else:
                rated.value = request.data['value']
                rated.save()
        except ObjectDoesNotExist:
            ser.save()
        comic = models.Comic.objects.get(pk=request.data["comic_id"])
        ratings = models.Rating.objects.filter(comic_id=request.data["comic_id"])
        average = find_average(ratings.iterator())
        comic.rating = round(average, 1)
        comic.save()
        return Response(ser.data, status=status.HTTP_200_OK)



class GetRating(APIView):
    def get(self, request, pk, *args):
        ratings = models.Rating.objects.select_related('comic_id').filter(comic_id=pk)
        average = find_average(ratings.iterator())
        return Response({'rating': round(average, 1)})
