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
    #@log_in_confirm
    def get(self, request, cafe_id):         
            cafe                 = Cafe.objects.get(id=cafe_id)
            menus                = Menu.objects.filter(cafe_id=cafe_id)
            reviews              = Review.objects.filter(
                cafe_id = cafe_id, comment_on_review_id__isnull = True
            )
            comment_in_reviews   = Review.objects.filter(
                cafe_id = cafe_id, comment_on_review_id__isnull = False
            )
            gallery_image_urls = CafeImage.objects.filter(cafe_id=cafe_id)
            star_ratings = StarRating.objects.filter(cafe_id=cafe_id)

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
                    'id'               : review.user_id,
                    'nickname'         : User.objects.get(id=review.user_id).nickname,
                    'profile_image'    : User.objects.get(id=review.user_id).image_url,
                    'star_rating'      : StarRating.objects.get(
                        cafe_id = cafe_id, user_id = review.user_id
                        ).score,
                    'content'          : review.content,
                    'review_like'      : ReviewLike.objects.filter(review_id=review.id).count(),
                    'comment_on_review': len(comment_in_review_list)
                }
                )
            
            informations = []

            gallery_image_list = []

            if star_ratings.exists():
                star_rating_value = StarRating.objects.values('cafe_id', 'score')            
                cafe_avg_rating = star_rating_value.values('cafe_id').annotate(avg_score=Avg('score'))
                cafe_ranking = cafe_avg_rating.order_by('-avg_score')
                cafe_ranking_number = [x['cafe_id'] for x in list(cafe_ranking)].index(cafe_id) + 1
            else:
                cafe_ranking_number = None

            if star_ratings.exists():
                cafe_score = star_ratings.values('cafe_id', 'score')
                score_count = cafe_score.values('score').annotate(count_score=Count('score'))
                max_ratings = score_count.order_by('-count_score')
                max_ratings_count = [x['count_score'] for x in list(max_ratings)][0]
            else:
                max_ratings_count = None
            
            if reviews.exists():
                review_count = reviews.values('cafe_id').annotate(cnt=Count('id'))
                review_ranking_number = [x['cafe_id'] for x in list(review_count)].index(cafe_id) + 1
            else:
                review_ranking_number = None

            for gallery_image_url in gallery_image_urls:
                gallery_image_list.append({
                    'index' : gallery_image_url.id, 
                    'img' : gallery_image_url.image_url
                }
                )

            if not star_ratings.exists():
                if reviews.exists():
                    informations.append(
                    {   
                        'id'                 : cafe_id,
                        'name'               : cafe.name,
                        'business_hour'      : cafe.business_hours,
                        'address'            : cafe.address,
                        'phone_number'       : cafe.phone_number,
                        'description'        : cafe.description,
                        'review_ranking'     : review_ranking_number,
                        'likes'              : CafeLike.objects.filter(cafe_id=cafe_id).count(),
                        'cafe_image_url'     : cafe.main_image_url,
                        'gallery_image'      : gallery_image_list,
                        'evaluation_graphs'  : [{
                            '0.5' : '0',
                            '1.0' : '0',
                            '1.5' : '0',
                            '2.0' : '0',
                            '2.5' : '0',
                            '3.0' : '0',
                            '3.5' : '0',
                            '4.0' : '0',
                            '4.5' : '0',
                            '5.0' : '0',
                        }]                               
                    }
                )
            if not reviews.exists():
                informations.append(
                    {   
                        'id'                 : cafe_id,
                        'name'               : cafe.name,
                        'business_hour'      : cafe.business_hours,
                        'address'            : cafe.address,
                        'phone_number'       : cafe.phone_number,
                        'description'        : cafe.description,
                        'likes'              : CafeLike.objects.filter(cafe_id=cafe_id).count(),
                        'cafe_image_url'     : cafe.main_image_url,
                        'gallery_image': gallery_image_list,
                        'evaluation_graphs'  : [{
                            '0.5' : '0',
                            '1.0' : '0',
                            '1.5' : '0',
                            '2.0' : '0',
                            '2.5' : '0',
                            '3.0' : '0',
                            '3.5' : '0',
                            '4.0' : '0',
                            '4.5' : '0',
                            '5.0' : '0',
                        }]                                
                    }
                )

            if star_ratings.exists():
                if reviews.exists():
                    informations.append(
                    {   
                        'id'                 : cafe_id,
                        'name'               : cafe.name,
                        'business_hour'      : cafe.business_hours,
                        'address'            : cafe.address,
                        'phone_number'       : cafe.phone_number,
                        'description'        : cafe.description,
                        'star_rating_ranking': cafe_ranking_number,
                        'average_star_rating': star_ratings,
                        'likes'              : CafeLike.objects.filter(cafe_id=cafe_id).count(),
                        'cafe_image_url'     : cafe.main_image_url,
                        'gallery_image'      : gallery_image_list,
                        'evaluation_graphs'  : [{
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

                if not reviews.exists():
                    informations.append(
                    {   
                        'id'                 : cafe_id,
                        'name'               : cafe.name,
                        'business_hour'      : cafe.business_hours,
                        'address'            : cafe.address,
                        'phone_number'       : cafe.phone_number,
                        'description'        : cafe.description,
                        'star_rating_ranking': cafe_ranking_number,
                        'average_star_rating': star_ratings,
                        'likes'              : CafeLike.objects.filter(cafe_id=cafe_id).count(),
                        'cafe_image_url'     : cafe.main_image_url,
                        'gallery_image'      : gallery_image_list,
                        'evaluation_graphs'  : [{
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

                average_score = StarRating.objects.filter(
                    cafe_id=recommended_cafe.id
                    ).aggregate(average = Avg('score'))['average']

                if average_score != None:
                    recommendation.append({
                        'cafe_name'          : recommended_cafe.name,
                        'average_star_rating': '{:.1f}'.format(average_score),
                        'url'                : recommended_cafe.main_image_url
                    }   
                    )
                else:
                    recommendation.append({
                        'cafe_name'          : recommended_cafe.name,
                        'average_star_rating': '0',
                        'url'                : recommended_cafe.main_image_url
                    }   
                    )

            return JsonResponse({
                    'menus'         : menu_list,
                    'review'        : review_list,
                    'informations'  : informations,
                    'recommendation': recommendation,
                    }, status=200)    
            


