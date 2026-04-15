from django.urls import path
from .views import preregister_user_view, egister_rdp_connection_view

urlpatterns = [
    path("api/preregister/", preregister_user_view, name="preregister_user"),
    path("api/rdp-connection/<str:container_connected_name>/<int:identifier>/", egister_rdp_connection_view, name="register_rdp_connection"),
]