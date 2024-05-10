from functools import wraps
from django.http import HttpResponseForbidden

def is_authenticated(request):
    if request.COOKIES.get('is_authenticated') == "True":
        return True
    return False

def get_current_user(request):
    username = request.COOKIES.get('username')
    negara = request.COOKIES.get('negara')
    context = {
        'username': username,
        'user_role': negara,
    }
    return context
