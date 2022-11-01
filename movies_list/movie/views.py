from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.core.paginator import Paginator

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Movie, Collection, RequestCount
from .serializers import MovieSerializer, CollectionSerializer, RequestCountSerializer
from .forms import UserRegistrationForm

import requests
from collections import Counter


# Retrieving data from API

URL = 'https://demo.credy.in/api/v1/maya/movies/'
NO_OF_MOVIES_PER_PAGE = 10
all_movies = []

def get_response(URL, x):
    response = requests.get(URL + f'?page={x}')
    return response.json()
    
def get_movie_count(data):
    return data['count']

def get_movie_data(response):
    movies_list = []
    for item in response['results']:
        movie = {
            'title': item['title'],
            'description': item['description'],
            'genres': item['genres'],
            'uuid': item['uuid']
        }
    movies_list.append(movie)
    return movies_list

def movie_list_first(request):
    return movie_list(request, 1)

def get_genres(request):
    user_id = request.user.id
    genre_dict = {}
    for queryset in Collection.objects.filter(user=user_id):
        for movie in queryset.movies.all():
            print(movie)
            if movie.genre not in genre_dict:
                genre_dict[i.movies.genre] = 1
            else:
                genre_dict[i.movies.genre] += 1
    
    temp = Counter(genre_dict)
    result = []
    for i in range(len(temp.most_common(3))):
        result.append(temp.most_common(3)[i][0])

    return result
        

def home(request):
    return render(request, 'movie/home.html')
    

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            form.save()
            messages.success(request, f"Account has been created for {username}!")
            return redirect('login-user')
    else:
        form = UserRegistrationForm()    
    return render(request, 'user/register.html', {'form': form})

class MovieList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        data = get_response(URL, page)
        page_count = get_movie_count(data)//NO_OF_MOVIES_PER_PAGE      
        return Response(data)


class CollectionDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Collection.objects.get(collection_uuid=pk)
        except Collection.DoesNotExist:
            raise Http404
        
    def get(self, request, pk, format=None):
        collection = self.get_object(pk)
        serializer = CollectionSerializer(collection)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        collection = self.get_object(pk)
        serializer = CollectionSerializer(collection, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        collection = self.get_object(pk)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CollectionList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        collection = Collection.objects.all()
        serializer = CollectionSerializer(collection, many=True)
        response = {
            "is_success": True,
            "data": {
                "collections": serializer.data
            },
            "favorite_genres": get_genres(request)
        }
        return Response(response)

    def post(self, request, format=None):
        serializer = CollectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "collection_uuid": serializer.data['collection_uuid']
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RequestCountList(APIView):
    def get(self, request):
        count = RequestCount.objects.all()
        serializer = RequestCountSerializer(count)
        response = {
            "requests": serializer.data['count']
        }
        return Response(response)

class RequestCountDetail(APIView):
    def get(self, request):
        count = RequestCount.objects.get(id=1)
        count.count = 0
        count.save()
        response = {
            "message": "request count reset successfully"
        }
        return Response(response, status=status.HTTP_200_OK)