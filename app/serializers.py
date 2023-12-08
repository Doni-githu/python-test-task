from rest_framework import serializers
from .models import *


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=200)
    email = serializers.EmailField(max_length=200)


class ComicSerializer(serializers.ModelSerializer):
    author_id = serializers.IntegerField(write_only=True)
    author = UserSerializer(read_only=True)
    rating = serializers.FloatField(read_only=True, default=0)

    class Meta:
        model = Comic
        fields = "__all__"

    def create(self, validated_data):
        data = {
            "title": validated_data["title"],
            "author": validated_data["author_id"],
        }
        return super().create(validated_data=validated_data)


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = "__all__"
