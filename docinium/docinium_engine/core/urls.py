from django.urls import path, include
from core import views
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.Login, name='login'),
    path('logout', views.Logout, name='logout'),
]
