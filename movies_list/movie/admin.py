from django.contrib import admin
from .models import Collection, Movie, RequestCount

admin.site.register(Collection)
admin.site.register(Movie)
admin.site.register(RequestCount)