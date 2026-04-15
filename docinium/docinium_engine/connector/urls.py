from django.urls import path
from .views import preregister_user_view, egister_rdp_connection_view , display_all_rdp_connections_view

urlpatterns = [
    path("api/preregister/", preregister_user_view, name="preregister_user"),
    path("api/rdp-connection/<str:container_connected_name>/<int:identifier>/<str:guacamole_client_token>/", egister_rdp_connection_view, name="register_rdp_connection"),
    path("api/containers/", display_all_rdp_connections_view, name="get_rdp_connections"),
]