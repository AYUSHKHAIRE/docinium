from django.urls import path
from .views import preregister_user_view

urlpatterns = [
    path("api/preregister/", preregister_user_view, name="preregister_user"),
]