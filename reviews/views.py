import json
from json.decoder import JSONDecodeError

from django.http.response import JsonResponse
from django.views         import View

from reviews.models import Review
from cafes.models   import Cafe
from users.models   import User
from utils          import log_in_confirm

class ReviewView(View):
    @log_in_confirm
    def post(self, request, cafe_id):
        try:
            if not Cafe.objects.filter(id=cafe_id).exists():
                return JsonResponse({'MESSAGE' : 'CAFE_DOES_NOT_EXIST'}, status=400)

            if Review.objects.filter(cafe_id=cafe_id, user_id=request.user.id).exists():
                return JsonResponse({'MESSAGE' : 'REVIEW_ALREADY_EXIST'})

            data    = json.loads(request.body)
            cafe    = Cafe.objects.get(id=cafe_id)
            content = data['content']

            if not content:
                return JsonResponse({'MESSAGE' : 'EMPTY_CONTENT'}, status=400)

            Review.objects.create(
                user    = request.user,
                cafe    = cafe,
                content = content
            )
            return JsonResponse({'MESSAGE' : 'REVIEW_CREATED'}, status=200)

        except KeyError:
            return  JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)

        except JSONDecodeError:
            return JsonResponse({'MESSAGE' : 'JSON_DECODE_ERROR'}, status=400)

    @log_in_confirm
    def delete(self, request, cafe_id):
        if not Review.objects.filter(cafe_id=cafe_id).exists():
            return JsonResponse({'MESSAGE' : 'CAFE_DOSE_NOT_EXIST'}, status=400)

        if not Review.objects.filter(cafe_id=cafe_id, user_id=request.user.id).exists():
            return JsonResponse({'MESSAGE' : 'REVIEW_DOES_NOT_EXIST'}, status=400)

        Review.objects.filter(cafe_id=cafe_id, user_id=request.user.id).delete()
        return JsonResponse({'MESSAGE' : 'REVIEW_DELETED'}, status=200)

        