import json

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Count

from reviews.models import Review
from cafes.models   import Cafe


class ReviewRankingView(View):
    def get(self, request):
        cafe_reviews           = Review.objects.filter(comment_on_review_id__isnull=True).values('cafe_id').annotate(cnt=Count('id'))
        review_ranking         = list(cafe_reviews.order_by('-cnt'))
        review_ranking_results = []

        if len(review_ranking) > 10:
            for i in range(10):
                cafe_id           = Cafe.objects.get(id=review_ranking[i]['cafe_id']).id
                cafe_review_count = review_ranking[i]['cnt']

                review_ranking_results.append({
                    'cafe_id'           : cafe_id,
                    'cafe_name'         : Cafe.objects.get(id=cafe_id).name,
                    'cafe_image'        : Cafe.objects.get(id=cafe_id).main_image_url,
                    'cafe_address'      : Cafe.objects.get(id=cafe_id).address,
                    'cafe_review_counts': cafe_review_count
                })
        else:
            for i in range(cafe_reviews.count()):
                cafe_id           = Cafe.objects.get(id=review_ranking[i]['cafe_id'])
                cafe_review_count = review_ranking[i]['cnt']

                review_ranking_results.append({
                    'cafe_id'           : cafe_id,
                    'cafe_name'         : Cafe.objects.get(id=cafe_id).name,
                    'cafe_image'        : Cafe.objects.get(id=cafe_id).main_image_url,
                    'cafe_address'      : Cafe.objects.get(id=cafe_id).address,
                    'cafe_review_counts': cafe_review_count
                })

        return JsonResponse({'REVIEW_RANKING': review_ranking_results}, status=200)