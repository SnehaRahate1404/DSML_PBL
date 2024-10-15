# views.py
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie  # Ensures that a CSRF cookie is set on the response
def get_csrf_token(request):
    print("requested for token")
    csrf_token = get_token(request)
    print(csrf_token)
    return JsonResponse({'csrfToken': csrf_token})