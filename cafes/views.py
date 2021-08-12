import json
from json.decoder import JSONDecodeError

from django.http.response import JsonResponse
from django.views         import View
from django.db.models     import Count, Avg, Q

from reviews.models import Review
from cafes.models   import Cafe, Menu
from ratings.models import StarRating
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
        reviews = Review.objects.filter(cafe_id=cafe_id).annotate(like_count=Count('reviewlike')).order_by('-like_count')

        review_list = [{   
                'id'                : review.user_id,
                'nickname'          : review.user.nickname,
                'profile_image'     : review.user.image_url,
                'star_rating'       : review.user.starrating_set.get(cafe_id=cafe_id).score,
                'content'           : review.content,
                'review_like'       : review.like_count,
                'comment_on_review' : review.comment_on_review.count() if review.comment_on_review else 0
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

        star_rating = StarRating.objects.values('cafe_id').annotate(cnt=Count('score'), avg=Avg('score')).filter(cafe_id=cafe_id)

        results = {
            'total_count' : star_rating[0]['cnt'] if star_rating.exists() else 0,
            'average'   : '{:.1f}'.format(star_rating[0]['avg']) if star_rating.exists() else 0
        }

        return JsonResponse({'result':results}, status=200)

class CafeView(View):
    def get(self, request, cafe_id):
        if not Cafe.objects.filter(id=cafe_id).exists():
            return JsonResponse({'MESSAGE':'CAFE_DOES_NOT_EXIST'}, status=404)
            
        cafe = Cafe.objects.annotate(
            avg_score = Avg('starrating__score'),
            A = Count('starrating', filter=Q(starrating__score=0.5)),
            B = Count('starrating', filter=Q(starrating__score=1.0)),
            C = Count('starrating', filter=Q(starrating__score=1.5)),
            D = Count('starrating', filter=Q(starrating__score=2.0)),
            E = Count('starrating', filter=Q(starrating__score=2.5)),
            F = Count('starrating', filter=Q(starrating__score=3.0)),
            G = Count('starrating', filter=Q(starrating__score=3.5)),
            H = Count('starrating', filter=Q(starrating__score=4.0)),
            I = Count('starrating', filter=Q(starrating__score=4.5)),
            J = Count('starrating', filter=Q(starrating__score=5.0)),
        ).get(id=cafe_id)

        cafe_rating = Cafe.objects.annotate(avg_score=Avg('starrating__score')).filter(avg_score__gt=0).values_list('id', flat=True).order_by('-avg_score')
        cafe_ranking = list(cafe_rating).index(cafe_id) + 1 if cafe_id in cafe_rating else None

        cafe_review = Cafe.objects.annotate(cnt=Count('review__id')).filter(cnt__gt=0).values_list('id', flat=True).order_by('-cnt')
        review_ranking = list(cafe_review).index(cafe_id) + 1 if cafe_id in cafe_review else None

        gallery_images = [{'index':image.id, 'img':image.image_url} for image in cafe.cafeimage_set.all()]

        informations = {
            'id'                 : cafe_id,
            'name'               : cafe.name,
            'business_hour'      : cafe.business_hours,
            'address'            : cafe.address,
            'phone_number'       : cafe.phone_number,
            'description'        : cafe.description,
            'star_rating_ranking': cafe_ranking,
            'review_ranking'     : review_ranking,
            'likes'              : cafe.cafelike_set.all().count(),
            'cafe_image_url'     : cafe.main_image_url,
            'background_image'   : gallery_images[0], 
            'gallery_image'      : gallery_images,
            'evaluation_graphs'  : [cafe.A, cafe.B, cafe.C, cafe.D, cafe.E, cafe.F, cafe.G, cafe.H, cafe.I, cafe.J]                              
        }
        return JsonResponse({'informations':informations}, status=200)