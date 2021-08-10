import json
from json.decoder import JSONDecodeError

from django.http.response import JsonResponse
from django.views         import View
from django.db.models     import Count, Avg

from reviews.models import Review
from cafes.models   import Cafe
from utils          import log_in_confirm

"""
/cafes
/cafes?ordering=-review_count
/cafes?ordering=-avg_rating
"""

class CafeListView(View):
    def get(self, request):
        ordering = request.GET.get('ordering', None)
        cafes = Cafe.objects.all().values('id').annotate(avg_rating=Avg('starrating__score')).order_by('-avg_rating')
        results = []
        cnt = 0
        
        if ordering == '-review_count':
            cafes_review_count = Cafe.objects.all().annotate(review_count=Count('review')).order_by('-review_count')

            for cafe in cafes_review_count:
                if cnt == 10:
                    break
                cafe_id = cafe.id
                this = Cafe.objects.get(id=cafe_id)

                results.append({
                    'id' : cafe_id,
                    'name' : this.name,
                    'address' : this.address,
                    'image' : this.main_image_url,
                    'avg_rating' : '%.1f' % cafes.get(id=cafe_id)['avg_rating']
                })

                cnt += 1


        if ordering == '-avg_rating':
            for cafe in cafes:
                if cnt == 10:
                    break

                cafe_id = cafe['id']
                this = Cafe.objects.get(id=cafe_id)

                results.append({
                    "id"        : cafe_id,
                    "name"      : this.name,
                    "address"   : this.address,
                    "image"     : this.main_image_url,
                    "avg_rating": '%.1f' % cafe['avg_rating']
                })

                cnt += 1

        return JsonResponse({'CAFE_LIST': results}, status=200)

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


"""
SELECT 
    c.id, 
    c.name, 
    COUNT(r.id) AS review_count, 
    AVG(sr.score) AS avg_rating 
FROM cafes c 
LEFT OUTER JOIN reviews r ON c.id = r.cafe_id 
LEFT OUTER JOIN star_ratings sr ON c.id = sr.cafe_id 
GROUP BY c.id;
"""
