import json

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Count, Avg

from ratings.models import StarRating
from cafes.models   import Cafe


class RatingRankingView(View):
    def get(self, request):
        cafe_avg_rating      = StarRating.objects.values('cafe_id').annotate(avg_rating=Avg('score'))
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