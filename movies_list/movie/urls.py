from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('', views.home),
    path('register/', views.register, name='register-user'),
    path('login/', LoginView.as_view(template_name='user/login.html'), name='login-user'),
    path('logout/', LogoutView.as_view(template_name='user/logout.html'), name='logout-user'),
    path('collection/', views.CollectionList.as_view()),
    path('collection/<str:pk>', views.CollectionDetail.as_view()),
    path('movies/', views.MovieList.as_view()),
    path('movies/<int:pk>', views.MovieList.as_view()),
    path('request-count/', views.RequestCountList.as_view()),
    path('request-count/reset/', views.RequestCountDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)