import json
from json.decoder import JSONDecodeError

from django.http.response import JsonResponse
from django.views         import View
from django.db.models     import Count

from reviews.models import Review
from cafes.models   import Cafe
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