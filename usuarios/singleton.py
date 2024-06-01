from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

class UserAuthSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(UserAuthSingleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def login_user(self, request, username, password):
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return True
        else:
            return False
