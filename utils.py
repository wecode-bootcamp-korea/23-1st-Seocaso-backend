import jwt

from django.http import JsonResponse

from users.models import User
from my_settings import SECRET_KEY

def LoginConfirm(func):
    def wrapper(self, request, *args, **kwargs):
        user_token = request.headers.get('Authorization')
        header = jwt.decode(user_token, SECRET_KEY, algorithms='HS256')

        if not User.objects.filter(id=header['id']).exists():
            return JsonResponse({'MESSAGE' : 'INVALID_USER'}, status=401)

        request.user = User.objects.get(id=header['id'])

        return func(self, request, *args, **kwargs)

    return wrapper
