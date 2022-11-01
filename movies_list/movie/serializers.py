from rest_framework import serializers
from .models import Movie, Collection, RequestCount

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields =['movie_uuid', 'title', 'description', 'genre']

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['title', 'collection_uuid', 'description']


class RequestCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestCount
        fields = ['count']