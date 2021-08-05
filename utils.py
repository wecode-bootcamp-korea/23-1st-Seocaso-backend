import jwt

from django.http  import JsonResponse

from users.models import User
from my_settings  import SECRET_KEY, ALGORITHM

def log_in_confirm(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            user_token = request.headers.get('Authorization')
            user       = jwt.decode(user_token, SECRET_KEY, algorithms=ALGORITHM)

            if not User.objects.filter(id=user['id']).exists():
                return JsonResponse({'MESSAGE' : 'INVALID_USER'}, status=404)

            request.user = User.objects.get(id=user['id'])

            return func(self, request, *args, **kwargs)

        except jwt.InvalidSignatureError:
            return JsonResponse({'MESSAGE' : 'JWT_SIGNATURE_ERROR'}, status=400)

        except jwt.DecodeError:
            return JsonResponse({'MESSAGE' : 'JWT_DECODE_ERROR'}, status=400)

    return wrapper