import json

from django.http  import JsonResponse
from django.views import View
from django.db.models import Avg, Count

from cafes.models   import Cafe, Menu, CafeImage
from likes.models   import CafeLike, ReviewLike
from ratings.models import StarRating
from reviews.models import Review
from users.models   import User
from utils          import log_in_confirm

class CafeDetailView(View):
    @log_in_confirm
    def get(self, request, cafe_id):
        try:          
            cafe                 = Cafe.objects.get(id=cafe_id)
            menus                = Menu.objects.filter(cafe_id=cafe_id)
            reviews              = Review.objects.filter(
                cafe_id = cafe_id, comment_on_review_id__isnull = True
            )
            comment_in_reviews   = Review.objects.filter(
                cafe_id = cafe_id, comment_on_review_id__isnull = False
            )
            background_image_urls = CafeImage.objects.filter(cafe_id=cafe_id)

            menu_list = []

            for menu in menus:
                menu_list.append(
                {
                    'id'       : menu.id,
                    'url'      : menu.image_url,
                    'menu_name': menu.name,
                    'price'    : '{:.0f}원'.format(menu.price)
                }
                )

            review_list = []

            for review in reviews:
                
                comment_in_review_list = []

                for comment_in_review in comment_in_reviews:

                    comment_in_review_list.append(
                        {
                            'comment_in_review' : comment_in_review.content 
                        }
                    )

                review_list.append(
                {
                    'nickname'         : User.objects.get(id=review.user_id).nickname,
                    'profile_image'    : User.objects.get(id=review.user_id).image_url,
                    'star_rating'      : StarRating.objects.get(user_id=review.user_id).score,
                    'content'          : review.content,
                    'review_like'      : ReviewLike.objects.filter(review_id=review.id).count(),
                    'comment_on_review': len(comment_in_review_list)
                }
                )
            
            informations = []

            background_image_url_list = []

            star_ratings = StarRating.objects.values('cafe_id', 'score')            
            cafe_avg_rating = star_ratings.values('cafe_id').annotate(avg_score=Avg('score'))
            cafe_ranking = cafe_avg_rating.order_by('-avg_score')
            cafe_ranking_number = [x['cafe_id'] for x in list(cafe_ranking)].index(cafe_id) + 1
            
            review_count = reviews.values('cafe_id').annotate(cnt=Count('id'))
            review_ranking = review_count.order_by('-cnt')
            review_ranking_number = [x['cafe_id'] for x in list(review_ranking)].index(cafe_id) + 1

            cafe_score = StarRating.objects.filter(cafe_id=cafe_id).values('cafe_id', 'score')
            score_count = cafe_score.values('score').annotate(count_score=Count('score'))
            max_ratings = score_count.order_by('-count_score')
            max_ratings_count = [x['count_score'] for x in list(max_ratings)][0] + 1 

            for background_image_url in background_image_urls:
                background_image_url_list.append(
                    background_image_url.image_url
                )

            informations.append(
                {   
                    'id'                  : cafe_id,
                    'name'                : cafe.name,
                    'business_hour'       : cafe.business_hours,
                    'address'             : cafe.address,
                    'phone_number'        : cafe.phone_number,
                    'description'         : cafe.description,
                    'review_ranking'      : review_ranking_number,
                    'star_rating_ranking' : cafe_ranking_number,
                    'likes'               : CafeLike.objects.filter(cafe_id=cafe_id).count(),
                    'cafe_image_url'      : cafe.main_image_url,
                    'background_image_url': background_image_url_list,
                    'evaluation_graphs'   : [{
                        '0.5' : '{:.2f}'.format(StarRating.objects.filter(
                            cafe_id=cafe_id, score=0.5
                            ).count() / max_ratings_count),
                        '1.0' : '{:.2f}'.format(StarRating.objects.filter(
                            cafe_id=cafe_id, score=1.0
                            ).count() / max_ratings_count),
                        '1.5' : '{:.2f}'.format(StarRating.objects.filter(
                            cafe_id=cafe_id, score=1.5
                            ).count() / max_ratings_count),
                        '2.0' : '{:.2f}'.format(StarRating.objects.filter(
                            cafe_id=cafe_id, score=2.0
                            ).count() / max_ratings_count),
                        '2.5' : '{:.2f}'.format(StarRating.objects.filter(
                            cafe_id=cafe_id, score=2.5
                            ).count() / max_ratings_count),
                        '3.0' : '{:.2f}'.format(StarRating.objects.filter(
                            cafe_id=cafe_id, score=3.0
                            ).count() / max_ratings_count),
                        '3.5' : '{:.2f}'.format(StarRating.objects.filter(
                            cafe_id=cafe_id, score=3.5
                        ).count() / max_ratings_count),
                        '4.0' : '{:.2f}'.format(StarRating.objects.filter(
                            cafe_id=cafe_id, score=4.0
                            ).count() / max_ratings_count),
                        '4.5' : '{:.2f}'.format(StarRating.objects.filter(
                            cafe_id=cafe_id, score=4.5
                            ).count() / max_ratings_count),
                        '5.0' : '{:.2f}'.format(StarRating.objects.filter(
                            cafe_id=cafe_id, score=5.0
                            ).count() / max_ratings_count),
                    }]                               
                }
            )

            recommendation = []

            cafe_info = Cafe.objects.get(id=cafe_id)

            recommended_cafes = Cafe.objects.filter(address__icontains=cafe_info.address[:5])[:6] 

            for recommended_cafe in recommended_cafes:

                average_score = StarRating.objects.filter(cafe_id=recommended_cafe.id).aggregate(average = Avg('score'))['average']

                if average_score != None:
                    recommendation.append({
                        'cafe_name'          : recommended_cafe.name,
                        'average_star_rating': '{:.1f}'.format(average_score),
                        'cafe_image'         : recommended_cafe.main_image_url
                    }   
                    )
                else:
                    recommendation.append({
                        'cafe_name'          : recommended_cafe.name,
                        'average_star_rating': '0',
                        'cafe_image'         : recommended_cafe.main_image_url
                    }   
                    )

            datas = []
            
            datas.append(
                {
                    'menus'         : menu_list,
                    'reviews'       : review_list,
                    'informations'  : informations,
                    'recommendation': recommendation,
                }
            )

            return JsonResponse({'data':datas}, status=200)

        except ValueError:
            return JsonResponse({'MESSAGE':'VALUE_ERROR'}, status=400)        
            


