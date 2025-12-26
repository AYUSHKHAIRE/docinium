# connector/services.py
from django.contrib.auth import get_user_model
from django.db import transaction
from .models import CustomToken

User = get_user_model()

@transaction.atomic
def preregister_user(username: str, password: str | None = None, email: str | None = None):
    """
    Pre-register a user and create a custom token.
    No signals. Fully internal.
    """
    if User.objects.filter(username=username).exists():
        preuser = User.objects.filter(username=username)
        preuser.delete()

    user = User.objects.create_user(username=username, password=password, email=email)
    token = CustomToken.objects.create(user=user)
    _id = token._id
    return user, _id, token.key
