import json

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from .services import preregister_user


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
