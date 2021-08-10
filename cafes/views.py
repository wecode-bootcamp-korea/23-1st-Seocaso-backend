import json
from json.decoder import JSONDecodeError

from django.http.response import JsonResponse
from django.views         import View

from reviews.models import Review
from cafes.models   import Cafe
from ratings.models import StarRating
from utils          import log_in_confirm

class ReviewView(View):
    @log_in_confirm
    def post(self, request, cafe_id):
        try:
            if Review.objects.filter(cafe_id=cafe_id, user_id=request.user.id).exists():
                return JsonResponse({'MESSAGE' : 'REVIEW_ALREADY_EXIST'}, status=400)

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
            return JsonResponse({'MESSAGE' : 'REVIEW_CREATED'}, status=201)

        except KeyError:
            return  JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)

        except JSONDecodeError:
            return JsonResponse({'MESSAGE' : 'JSON_DECODE_ERROR'}, status=400)

    @log_in_confirm
    def delete(self, request, cafe_id):
        review = Review.objects.filter(cafe_id=cafe_id, user_id=request.user.id)
        if not review.exists():
            return JsonResponse({'MESSAGE' : 'REVIEW_DOES_NOT_EXIST'}, status=400)

        review.delete()
        return JsonResponse({'MESSAGE' : 'REVIEW_DELETED'}, status=204)
    
class CommentOnReviewView(View):
    @log_in_confirm
    def post(self, request, review_id):
        data    = json.loads(request.body)

        if not Review.objects.filter(id=review_id).exists(): 
            return JsonResponse({'MESSAGE':'REVIEW_DOES_NOT_EXIST'}, status=404)
            
        cafe_id = Review.objects.get(id=review_id).cafe_id

        Review.objects.create(
            content              = data['content'],
            cafe_id              = cafe_id,
            comment_on_review_id = review_id,
            user                 = request.user
    )

        return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)

class StarRatingView(View):
    @log_in_confirm
    def post(self, request, cafe_id):
        try:
            data = json.loads(request.body)

            user = request.user

            if not Cafe.objects.filter(id=cafe_id).exists():
                return JsonResponse({'MESSAGE':'CAFE_DOES_NOT_EXIST'}, status=401)

            star, flag = StarRating.objects.get_or_create(cafe_id=cafe_id, user_id=user.id)

            if not flag:
                if star.score == data['score']:
                    star.delete()
                    return JsonResponse({'MESSAGE' : 'SCORE_DELETED'}, status=200)

                else:
                    star.score = data['score']
                    star.save()
                    return JsonResponse({'MESSAGE' : 'SCORE_UPDATED'}, status=200)
            else:
                StarRating.objects.filter(cafe_id=cafe_id, user_id=user.id).update(score=data['score'])
                return JsonResponse({'MESSAGE' : 'SCORE_CREATED'}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

        except JSONDecodeError:
            return JsonResponse({'MESSAGE':'JSON_DECODE_ERROR'}, status=400)

    def get(self, request, cafe_id):

        star_ratings = StarRating.objects.filter(cafe_id=cafe_id)

        results = []

        for star_rating in star_ratings:
            results.append(
                {
                    'score': star_rating.score,
                    'cafe_id' : star_rating.cafe_id,
                    'user_id' : star_rating.user_id
                }
            )

        return JsonResponse({'result':results}, status=200)