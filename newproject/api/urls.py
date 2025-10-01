from django.urls import path
from .views import create_user, get_users

urlpatterns = [
    path('user/', get_users, name='get-users'),
    path('user/create/', create_user, name='create-user'),
]