import json
from json.decoder import JSONDecodeError

from django.http.response import JsonResponse
from django.views         import View
from django.db.models     import Count, Avg

from reviews.models import Review
from cafes.models   import Cafe
from ratings.models import StarRating
from likes.models   import ReviewLike
from users.models   import User
from utils          import log_in_confirm

class CafeListView(View):
    def get(self, request):
        ordering = request.GET.get('ordering', None)
        order    = {
            "high_rating": "-avg_rating",
            "high_count" : "-review_count"
        }

        cafes   = Cafe.objects.all().annotate(review_count=Count('review', distinct=True))\
                                    .annotate(avg_rating=Avg('starrating__score', distinct=True))\
                                    .order_by(order.get(ordering, 'id'))[:10]

        results = [ {
            'id' : cafe.id,
            'name' : cafe.name,
            'image' : cafe.main_image_url,
            'address' : cafe.address,
            'avg_rating' : '%.1f' % cafe.avg_rating
        } for cafe in cafes ]

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

    def get(self, request, cafe_id):
        reviews = Review.objects.filter(cafe_id = cafe_id, comment_on_review_id__isnull = True)

        review_list = [{   
                'id'                : review.user_id,
                'nickname'          : User.objects.get(id=review.user_id).nickname,
                'profile_image'     : User.objects.get(id=review.user_id).image_url,
                'star_rating'       : StarRating.objects.get(
                    cafe_id = cafe_id, user_id = review.user_id
                    ).score,
                'content'           : review.content,
                'review_like'       : ReviewLike.objects.filter(review_id=review.id).count(),
                'comment_on_review' : Review.objects.filter(comment_on_review_id = review.id).count()
                } for review in reviews
            ]
        return JsonResponse({'reviews':review_list}, status=200)

class RatingCountView(View):
    def get(self, request):
        return JsonResponse({'RATINGS_COUNT' : StarRating.objects.count()}, status=200)
    
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
