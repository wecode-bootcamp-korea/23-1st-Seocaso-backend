import json
from json.decoder import JSONDecodeError

from django.http.response import JsonResponse
from django.views         import View

from reviews.models import Review
from cafes.models   import Cafe
from utils          import log_in_confirm

class CommentOnReviewView(View):
    @log_in_confirm
    def post(self, request, review_id):
        
        data = json.loads(request.body)
        
        cafe_id = Review.objects.get(id=review_id).cafe_id

        Review.objects.create(
            content           = data['content'],
            cafe              = Cafe.objects.get(id=cafe_id),
            comment_on_review = Review.objects.get(id=review_id),
            user              = request.user
        )

        return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)
             
