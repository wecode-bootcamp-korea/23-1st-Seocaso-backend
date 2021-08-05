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

        like, flag = CafeLike.objects.get_or_create(
            cafe = Cafe.objects.get(id=cafe_id)
        )

        if not flag:
            like.delete()
            return JsonResponse({'MESSAGE' : 'LIKE_DELETED'}, status=200)

        else:
            CafeLike.objects.create(
                user = request.user,
                cafe = Cafe.objects.get(id=cafe_id)
            )
            return JsonResponse({'MESSAGE' : 'LIKE_CREATED'}, status=201)

        # if not Cafe.objects.filter(id=cafe_id).exists():
        #     return JsonResponse({'MESSAGE' : 'CAFE_NOT_FOUND'}, status=400)
        
        # if not CafeLike.objects.filter(cafe_id=cafe_id, user_id=request.user.id):
        #     CafeLike.objects.create(
        #         user = request.user,
        #         cafe = Cafe.objects.get(id=cafe_id)
        #     )
        #     return JsonResponse({'MESSAGE' : 'CREATED'}, status=201)
        
        # else:
        #     CafeLike.objects.filter(cafe_id=cafe_id, user_id=request.user.id).delete()
        #     return JsonResponse({'MESSAGE' : 'DELETED'}, status=200)

class ReviewLikeView(View):
    @log_in_confirm
    def post(self, request, review_id):
        if not Review.objects.filter(id=review_id).exists():
            return JsonResponse({'MESSAGE' : 'REVIEW_DOES_NOT_EXIST'}, status=400)

        if not ReviewLike.objects.filter(review_id=review_id, user_id=request.user.id).exists():
            ReviewLike.objects.create(
                user   = request.user,
                review = Review.objects.get(id=review_id)
            )
            return JsonResponse({'MESSAGE' : 'LIKE_CREATED'}, status=201)

        else:
            ReviewLike.objects.filter(review_id=review_id, user_id=request.user.id).delete()
            return JsonResponse({'MESSAGE' : 'LIKE_DELETED'}, status=200)
    