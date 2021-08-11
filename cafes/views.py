import json
from json.decoder import JSONDecodeError

from django.http.response import JsonResponse
from django.views         import View
<<<<<<< HEAD
from django.db.models     import Avg, Count

from reviews.models import Review
from cafes.models   import Cafe
from cafes.models   import CafeImage 
from ratings.models import StarRating
from likes.models   import CafeLike

=======
from django.db.models     import Count, Avg

from reviews.models import Review
from cafes.models   import Cafe, Menu
>>>>>>> 71c90df174bc1fc84353a5badc657f27f5c2f30e
from utils          import log_in_confirm
from ratings.models import StarRating

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

<<<<<<< HEAD
        return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)  
            
class CafeInformationView(View):
    def get(self, request, cafe_id):
        if not Cafe.objects.filter(id=cafe_id).exists():
            return JsonResponse({'MESSAGE':'CAFE_DOES_NOT_EXIST'}, status=404)
            
        cafe                 = Cafe.objects.get(id=cafe_id)
        reviews              = Review.objects.filter(
            cafe_id = cafe_id, comment_on_review_id__isnull = True
        )
        gallery_image_urls = CafeImage.objects.filter(cafe_id=cafe_id)
        star_ratings = StarRating.objects.filter(cafe_id=cafe_id)
        
        if star_ratings.exists():
            star_rating_value = StarRating.objects.values('cafe_id', 'score')            
            cafe_avg_rating = star_rating_value.values('cafe_id').annotate(avg_score=Avg('score'))
            cafe_ranking = cafe_avg_rating.order_by('-avg_score')
            cafe_ranking_number = [x['cafe_id'] for x in list(cafe_ranking)].index(cafe_id) + 1
        else:
            cafe_ranking_number = None
        
        if reviews.exists():
            review_count = reviews.values('cafe_id').annotate(cnt=Count('id'))
            review_ranking_number = [x['cafe_id'] for x in list(review_count)].index(cafe_id) + 1
        else:
            review_ranking_number = None

        gallery_image_list = [{
                'index' : gallery_image_url.id, 
                'img' : gallery_image_url.image_url
            } for gallery_image_url in gallery_image_urls
        ]

        informations = {
            'id'                 : cafe_id,
            'name'               : cafe.name,
            'business_hour'      : cafe.business_hours,
            'address'            : cafe.address,
            'phone_number'       : cafe.phone_number,
            'description'        : cafe.description,
            'star_rating_ranking': cafe_ranking_number,
            'review_ranking'     : review_ranking_number,
            'likes'              : CafeLike.objects.filter(cafe_id=cafe_id).count(),
            'cafe_image_url'     : cafe.main_image_url,
            'background_image'   : gallery_image_list[0], 
            'gallery_image'      : gallery_image_list,
            'evaluation_graphs'  : [
                StarRating.objects.filter(cafe_id=cafe_id, score=0.5).count(),
                StarRating.objects.filter(cafe_id=cafe_id, score=1.0).count(),
                StarRating.objects.filter(cafe_id=cafe_id, score=1.5).count(),
                StarRating.objects.filter(cafe_id=cafe_id, score=2.0).count(),
                StarRating.objects.filter(cafe_id=cafe_id, score=2.5).count(),
                StarRating.objects.filter(cafe_id=cafe_id, score=3.0).count(),
                StarRating.objects.filter(cafe_id=cafe_id, score=3.5).count(),
                StarRating.objects.filter(cafe_id=cafe_id, score=4.0).count(),
                StarRating.objects.filter(cafe_id=cafe_id, score=4.5).count(),
                StarRating.objects.filter(cafe_id=cafe_id, score=5.0).count(),
            ]                              
        }
        return JsonResponse({'informations':informations}, status=200)
=======
        return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)

class MenuView(View):
    def get(self, request, cafe_id):
        menus = Menu.objects.filter(cafe_id=cafe_id)
        
        menu_list = [{
                'id'       : menu.id,
                'url'      : menu.image_url,
                'menu_name': menu.name,
                'price'    : '{:.0f}원'.format(menu.price)
            } for menu in menus
        ]
        return JsonResponse({'menus':menu_list}, status=200)
>>>>>>> 71c90df174bc1fc84353a5badc657f27f5c2f30e
