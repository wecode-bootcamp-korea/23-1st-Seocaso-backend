import json
from json.decoder import JSONDecodeError

from django.http.response import JsonResponse
from django.views         import View
from django.db.models     import Avg

from reviews.models import Review
from cafes.models   import Cafe
from utils          import log_in_confirm
from ratings.models import StarRating

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

class RatingRankingView(View):
    def get(self, request):
        cafe_avg_rating        = StarRating.objects.values('cafe_id').annotate(avg_rating=Avg('score'))
        rating_ranking         = list(cafe_avg_rating.order_by('-avg_rating'))
        rating_ranking_results = []

        if len(rating_ranking) > 10:
            for i in range(10):
                cafe_id    = rating_ranking[i]['cafe_id']
                avg_rating = '{0:.2g}'.format(rating_ranking[i]['avg_rating'])

                rating_ranking_results.append({
                    'cafe_id'        : cafe_id,
                    'cafe_name'      : Cafe.objects.get(id=cafe_id).name,
                    'cafe_image'     : Cafe.objects.get(id=cafe_id).main_image_url,
                    'cafe_address'   : Cafe.objects.get(id=cafe_id).address,
                    'cafe_avg_rating': avg_rating
                })
        
        else:
            for i in range(cafe_avg_rating.count()):
                cafe_id    = rating_ranking[i]['cafe_id']
                avg_rating = str(rating_ranking[i]['avg_rating'])[:3]

                rating_ranking_results.append({
                    'cafe_id'        : cafe_id,
                    'cafe_name'      : Cafe.objects.get(id=cafe_id).name,
                    'cafe_image'     : Cafe.objects.get(id=cafe_id).main_image_url,
                    'cafe_address'   : Cafe.objects.get(id=cafe_id).address,
                    'cafe_avg_rating': avg_rating
                })
        
        return JsonResponse({'RATING_RANKING_RESULTS' : rating_ranking_results})