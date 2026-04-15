import json
import os

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_exempt

from .services import preregister_user
from .models import rdpConnection , CustomToken

@csrf_exempt  # required since this is called from external client
@require_POST
def preregister_user_view(request):
    """
    HTTP endpoint to preregister a container user.
    """

    try:
        body = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON body"},
            status=400
        )

    username = body.get("username")
    password = body.get("password")

    if not username:
        return JsonResponse(
            {"error": "username is required"},
            status=400
        )

    try:
        user, user_id, token = preregister_user(
            username=username,
            password=password,
        )
    except ValueError as e:
        return JsonResponse(
            {"error": str(e)},
            status=409
        )
    except Exception as e:
        return JsonResponse(
            {"error": f"Failed to preregister user {e}"},
            status=500
        )

    return JsonResponse(
        {
            "user_id": user_id,
            "token": token,
        },
        status=201
    )

def get_user_from_token(request):
    auth = request.headers.get("Authorization")
    if not auth:
        return None
    try:
        prefix, token = auth.split()
        if prefix != "Token":
            return None
    except:
        return None
    try:
        token_obj = CustomToken.objects.get(key=token)
        return token_obj.user
    except CustomToken.DoesNotExist:
        return None

@csrf_exempt
def egister_rdp_connection_view(
    request, 
    container_connected_name,
    identifier,
    guacamole_client_token
):
    """
    HTTP endpoint to get the details of an RDP connection.
    """

    try:
        user = get_user_from_token(request)
        if not user:
            return JsonResponse(
                {"error": "Unauthorized"},
                status=401
            )
        connection = rdpConnection.objects.create(
            user=user,
            container_connected_name=container_connected_name,
            identifier=identifier,
            token=guacamole_client_token
        )
    except rdpConnection.DoesNotExist:
        return JsonResponse(
            {"error": "RDP connection not found"},
            status=404
        )

    return JsonResponse(
        {
            "user": connection.user.username,
            "container_connected_name": connection.container_connected_name,
            "identifier": connection.identifier,
        },
        status=200
    )
    
def display_all_rdp_connections_view(request):
    """
    HTTP endpoint to get the details of all RDP connections.
    """
    try:
        user = request.user
        if not user.is_authenticated:
            return JsonResponse(
                {"error": "Unauthorized"},
                status=401
            )
        connections = rdpConnection.objects.all()
        data = []
        for connection in connections:
            data.append({
                "user": connection.user.username,
                "container_connected_name": connection.container_connected_name,
                "identifier": connection.identifier,
                "guacamole_client_token": connection.token
            })
    except Exception as e:
        return JsonResponse(
            {"error": f"Failed to fetch RDP connections {e}"},
            status=500
        )
    return JsonResponse(
        {
            "connections": data
        },
        status=200
    )