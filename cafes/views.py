import json
from json.decoder import JSONDecodeError

from django.http.response import JsonResponse
from django.views         import View
from django.db.models     import Count, Avg

from reviews.models import Review
from cafes.models   import Cafe
from utils          import log_in_confirm

class UserCafeListView(View):
    def get(self, request, user_id):
        filter = request.GET.get('filter', None)

        results = []
        cafes_user_rated = Cafe.objects.filter(starrating__user_id=user_id)

        if not filter:
            for cafe in cafes_user_rated:
                results.append({
                    'id' : cafe.id,
                    'name' : cafe.name,
                    'address' : cafe.address,
                    'image' : cafe.main_image_url,
                    'like_count' : cafes_user_rated.annotate(like_count=Count('cafelike')).get(id=cafe.id).like_count
                })
            
            return JsonResponse({'CAFE_LIST' : results})
        
        if filter == '-avg_rating':
            avg_ranking = Cafe.objects.values('id').annotate(avg_rating=Avg('starrating__score')).order_by('-avg_rating')
            ids         = [ x['id'] for x in cafes_user_rated ]

            for cafe in avg_ranking:
                if cafe['id'] in ids:
                    cafe_id = cafe['id']
                    this    = Cafe.objects.get(id=cafe_id)

                    results.append({
                        'cafe_id' : cafe_id,
                        'cafe_name' : this.name,
                        'cafe_image' : this.main_image_url,
                        'cafe_address' : this.address,
                        'user_rating' : ,
                    })


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