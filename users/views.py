import json, re, bcrypt, jwt

from django.http  import JsonResponse
from django.views import View

from users.models import User
from my_settings  import SECRET_KEY, ALGORITHM

class SignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'message':'EMAIL_ALREADY_EXIST'}, status=400)

            NAME_VALIDATION     = re.compile('[\S]{2,}')
            EMAIL_VALIDATION    = re.compile('[a-z0-9-_.]+@[a-z]+\.[a-z]')
            PASSWORD_VALIDATION = re.compile('(?=.{10,})(?=.*[a-zA-Z!@#$%^&*()_+~])(?=.*[!@#$%^&*()_+~0-9]).*')
            
            if not NAME_VALIDATION.match(data['nickname']):
                return JsonResponse({'message':'NAME_FORMAT_ERROR'}, status=401)
            
            if not EMAIL_VALIDATION.match(data['email']):
                return JsonResponse({'message':'EMAIL_FORMAT_ERROR'}, status=401)
            
            if not PASSWORD_VALIDATION.match(data['password']):
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

        except json.decoder.JSONDecodeError:
            return JsonResponse({'message':'JSONDecodeError'}, status=400)

class SigninView(View):
    def post(self, request):
        try: 
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']
            
            user     = User.objects.get(email=email)

            if not User.objects.filter(email=email).exists():
                return JsonResponse({'MESSAGE' : "EMAIL DOESN'T EXIST"}, status=400)
            
            if not bcrypt.checkpw( password.encode('utf-8'), user.password.encode('utf-8') ):
                return JsonResponse({'MESSAGE' : 'WRONG PASSWORD'}, status=401)
            
            access_token = jwt.encode({'id' : user.id}, SECRET_KEY, algorithm=ALGORITHM)
            return JsonResponse({'TOKEN' : access_token}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)

        except json.decoder.JSONDecodeError:
            return JsonResponse({'MESSAGE':'JSONDecodeError'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'MESSAGE' : 'USER_DOES_NOT_EXIST'}, status=400)