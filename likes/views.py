from django.http  import JsonResponse
from django.views import View

from cafes.models import Cafe
from likes.models import CafeLike
from utils import LoginConfirm

class CafeLikeView(View):
    @LoginConfirm
    def post(self, request, cafe_id):
        if not Cafe.objects.filter(id=cafe_id).exists:
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
    
