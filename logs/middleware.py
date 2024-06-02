from threading import local
from django.utils.deprecation import MiddlewareMixin
from ipware import get_client_ip

_thread_locals = local()

def get_current_user():
    return getattr(_thread_locals, 'user', None)

class ThreadLocalMiddleware(MiddlewareMixin):
    def process_request(self, request):
        _thread_locals.user = request.user
        _thread_locals.request = request

def get_ip_address(request):
    ip, _ = get_client_ip(request)
    return ip
