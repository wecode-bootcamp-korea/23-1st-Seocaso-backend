import json, re, bcrypt

from django.http  import JsonResponse
from django.views import View

from users.models import User

class SignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'message':'EMAIL_ALREADY_EXIST'}, status=400)

            name_type     = re.compile('[\S]{2,}')
            email_type    = re.compile('[a-z0-9-_.]+@[a-z]+\.[a-z]')
            password_type = re.compile('(?=.{10,})(?=.*[a-zA-Z!@#$%^&*()_+~])(?=.*[!@#$%^&*()_+~0-9]).*')

            if not name_type.match(data['nickname']):
                return JsonResponse({'message':'NAME_FORMAT_ERROR'}, status=401)

            if not email_type.match(data['email']):
                return JsonResponse({'message':'EMAIL_FORMAT_ERROR'}, status=401)
            
            if not password_type.match(data['password']):
                return JsonResponse({'message':'PASSWORD_FORMAT_ERROR'}, status=401)

            hashed_password = bcrypt.hashpw(
                data['password'].encode('utf-8'),bcrypt.gensalt()
            ).decode()

            User.objects.create(
                nickname = data['nickname'],
                email    = data['email'],
                password = hashed_password
            )
            return JsonResponse({'message':'SUCCESS'}, status=201)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)