import json
from json.decoder import JSONDecodeError

from django.http.response import JsonResponse
from django.views         import View
from django.db.models     import Avg

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

class RecommendationView(View):
    def get(self, request, cafe_id):

        cafe = Cafe.objects.get(id=cafe_id)
        
        recommendation = []

        recommended_cafes = Cafe.objects.filter(address__icontains=cafe.address[:5]
        ).exclude(id=cafe_id)[:6] 

        for recommended_cafe in recommended_cafes:

            average_score = StarRating.objects.filter(
                cafe_id=recommended_cafe.id
                ).aggregate(average = Avg('score'))['average']

            if average_score != None:
                recommendation.append({
                    'cafe_id'            : recommended_cafe.id,
                    'cafe_name'          : recommended_cafe.name,
                    'average_star_rating': '{:.1f}'.format(average_score),
                    'url'                : recommended_cafe.main_image_url
                }   
                )
            else:
                recommendation.append({
                    'cafe_id'            : recommended_cafe.id,
                    'cafe_name'          : recommended_cafe.name,
                    'average_star_rating': '0',
                    'url'                : recommended_cafe.main_image_url
                }   
                )
        return JsonResponse({'recommendation':recommendation}, status=200)