from django.db import models
import uuid
from django.conf import settings

# Create your models here.
class Movie(models.Model):
    movie_uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    title = models.CharField(max_length=50)
    description = models.TextField()
    genre = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Collection(models.Model):
    collection_uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    title = models.CharField(max_length=50)
    description = models.TextField()
    movies = models.ManyToManyField(Movie)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.title

class RequestCount(models.Model):
    count = models.PositiveIntegerField()
    request = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.request