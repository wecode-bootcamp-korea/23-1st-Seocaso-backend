from django.http  import JsonResponse
from django.views import View

from cafes.models   import Cafe
from likes.models   import CafeLike, ReviewLike
from reviews.models import Review
from utils          import LoginConfirm

class CafeLikeView(View):
    @LoginConfirm
    def post(self, request, cafe_id):
        if not Cafe.objects.filter(id=cafe_id):
            return JsonResponse({'MESSAGE' : 'CAFE_DOES_NOT_EXIST'})

        if not CafeLike.objects.filter(cafe_id=cafe_id, user_id=request.user.id):
            CafeLike.objects.create(
                user = request.user,
                cafe = Cafe.objects.get(id=cafe_id)
            )
            return JsonResponse({'MESSAGE' : 'LIKE_CREATED'}, status=200)

        else:
            CafeLike.objects.filter(cafe_id=cafe_id, user_id=request.user.id).delete()
            return JsonResponse({'MESSAGE' : 'LIKE_DELETED'}, status=200)

class ReviewLikeView(View):
    @LoginConfirm
    def post(self, request, review_id):
        if not Review.objects.filter(id=review_id):
            return JsonResponse({'MESSAGE' : 'REVIEW_DOES_NOT_EXIST'}, status=400)

        if not ReviewLike.objects.filter(id=review_id, user_id=request.user.id):
            ReviewLike.objects.create(
                user   = request.user,
                review = Review.objects.get(id=review_id)
            )
            return JsonResponse({'MESSAGE' : 'LIKE_CREATED'}, status=200)

        else:
            ReviewLike.objects.filter(id=review_id, user_id=request.user.id).delete()
            return JsonResponse({'MESSAGE' : 'LIKE_DELETED'}, status=200)
    