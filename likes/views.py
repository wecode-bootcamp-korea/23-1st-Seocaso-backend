from json.encoder import JSONEncoder
from django.http  import JsonResponse
from django.views import View

from cafes.models   import Cafe
from likes.models   import CafeLike, ReviewLike
from reviews.models import Review
from users.models import User
from utils          import log_in_confirm

class CafeLikeView(View):
    @log_in_confirm
    def post(self, request, cafe_id):
        if not Cafe.objects.filter(id=cafe_id).exists:
            return JsonResponse({'MESSAGE' : 'CAFE_DOES_NOT_EXIST'}, status=400)

        like, flag = CafeLike.objects.get_or_create(cafe=Cafe.objects.get(id=cafe_id), user=request.user)

        if not flag:
            like.delete()
            return JsonResponse({'MESSAGE' : 'LIKE_DELETED'}, status=200)

        else:
            return JsonResponse({'MESSAGE' : 'LIKE_CREATED'}, status=201)

class ReviewLikeView(View):
    @log_in_confirm
    def post(self, request, review_id):
        if not Review.objects.filter(id=review_id).exists():
            return JsonResponse({'MESSAGE' : 'REVIEW_DOES_NOT_EXIST'}, status=400)

        like, flag = ReviewLike.objects.get_or_create(review=Review.objects.get(id=review_id), user=request.user)

        if not flag:
            like.delete()
            return JsonResponse({'MESSAGE' : 'LIKE_DELETED'}, status=200)
        
        else:
            return JsonResponse({'MESSAGE' : 'LIKE_CRAETED'}, status=201)
    